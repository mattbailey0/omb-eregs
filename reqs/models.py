from enum import Enum, unique

from django.db import models
from django.utils.translation import ugettext_lazy


class Agency(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = ugettext_lazy('Agency')
        verbose_name_plural = ugettext_lazy('Agencies')

    name = models.CharField(max_length=256)
    abbr = models.CharField(max_length=64, blank=True)
    omb_agency_code = models.CharField(max_length=8, blank=True)
    public = models.BooleanField(default=True)

    @property
    def name_with_abbr(self):
        if self.abbr:
            return '{0} ({1})'.format(self.name, self.abbr)
        return self.name

    def __str__(self):
        return self.name_with_abbr


class AgencyGroup(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = ugettext_lazy('Agency Group')
        verbose_name_plural = ugettext_lazy('Agency Groups')

    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=64, blank=True)
    agencies = models.ManyToManyField(Agency, related_name='groups',
                                      blank=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


@unique
class PolicyTypes(Enum):
    circular = 'Circular'
    executive = 'Executive Order'
    guidance = 'Guidance'
    hspd = 'HSPD'
    law = 'Law'
    memorandum = 'Memorandum'
    national_action = 'National Action Plan'
    plan = 'Plan'
    ppd = 'PPD'
    review = 'Policy Review'
    standards = 'Standards'
    strategy = 'Strategy'


class Office(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Policy(models.Model):
    class Meta:
        verbose_name_plural = ugettext_lazy('Policies')
        ordering = ['policy_number']

    policy_number = models.IntegerField(unique=True)
    title = models.CharField(max_length=1024)
    uri = models.CharField(max_length=256)
    omb_policy_id = models.CharField(max_length=64, blank=True)
    policy_type = models.CharField(
        max_length=32, choices=[(e.name, e.value) for e in PolicyTypes],
        blank=True
    )
    issuance = models.DateField()
    sunset = models.DateField(blank=True, null=True)
    policy_status = models.CharField(max_length=256, blank=True)
    document_source = models.FileField(blank=True)
    public = models.BooleanField(default=True)
    issuing_body = models.CharField(max_length=512)
    managing_office = models.ForeignKey(Office, on_delete=models.CASCADE,
                                        blank=True, null=True)

    @property
    def title_with_number(self):
        if self.omb_policy_id:
            return '{0}: {1}'.format(self.omb_policy_id, self.title)
        return self.title

    @property
    def original_url(self):
        if self.document_source:
            return self.document_source.url
        return self.uri

    @property
    def requirements_with_topics(self):
        return self.requirements.prefetch_related('topics').distinct()

    def __str__(self):
        text = self.title_with_number
        if len(text) > 100:
            text = text[:100] + '...'
        return '({0}) {1}'.format(self.policy_number, text)


class Requirement(models.Model):
    class Meta:
        ordering = ['req_id']

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE,
                               related_name='requirements')
    req_id = models.CharField(max_length=16, unique=True)
    policy_section = models.CharField(max_length=1024, blank=True)
    policy_sub_section = models.CharField(max_length=1024, blank=True)
    req_text = models.TextField()
    verb = models.CharField(max_length=1024, blank=True)
    impacted_entity = models.CharField(max_length=8192, blank=True)
    req_deadline = models.CharField(max_length=512, blank=True)
    citation = models.CharField(max_length=1024, blank=True)
    req_status = models.CharField(max_length=32, blank=True)
    precedent = models.CharField(max_length=1024, blank=True)
    related_reqs = models.CharField(max_length=1024, blank=True)
    omb_data_collection = models.CharField(max_length=1024, blank=True)
    public = models.BooleanField(default=True)
    agencies = models.ManyToManyField(Agency, blank=True)
    agency_groups = models.ManyToManyField(AgencyGroup, blank=True)
    topics = models.ManyToManyField(Topic, blank=True,
                                    related_name='requirements')
    all_agencies = models.ManyToManyField(
        Agency, through='RequirementAllAgencies',
        related_name='all_requirements')

    def __str__(self):
        text = self.req_text[:40]
        if len(self.req_text) > 40:
            text += '...'
        return '{0}: {1}'.format(self.req_id, text)

    def topic_names(self):
        return [topic.name for topic in self.topics.all()]


class RequirementAllAgencies(models.Model):
    """This many-to-many table refers to a view, allowing us to retrieve all
    agencies (including through the agency group relationship) relevant to a
    requirement (or vise versa)"""
    class Meta:
        db_table = 'reqs_requirement_all_agencies'
        managed = False

    id = models.CharField(max_length=1024, primary_key=True)    # noqa
    requirement = models.ForeignKey(Requirement, on_delete=models.DO_NOTHING)
    agency = models.ForeignKey(Agency, on_delete=models.DO_NOTHING)
