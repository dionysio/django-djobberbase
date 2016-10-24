# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.encoding import force_text
from django.urls import reverse
from django.conf import settings
from django.utils.functional import cached_property

from treebeard.mp_tree import MP_Node
from djobberbase.managers import ActiveJobsManager, TempJobsManager
from djobberbase.conf import settings as djobberbase_settings

class SlugMixin(models.Model):
    slug_field = ''

    slug = models.SlugField(blank=True, db_index=True)

    def get_slug(self, field):
        return slugify(field)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = self.get_slug(getattr(self, self.slug_field))
            setattr(self, self.slug_field, slug)
        super().save(self, *args, **kwargs)

    class Meta:
        abstract = True

class TreeNodeMixin:
    name_separator = ' > '
    path_separator = '/'

    @property
    def job_count(self):
        return self.jobs.count()

    @property
    def total_job_count(self):
        return sum(node.job_count for node in self.get_ancestors_and_self())

    @cached_property
    def full_name(self):
        return self.name_separator.join(str(node) for node in self.get_ancestors_and_self())

    @cached_property
    def reversed_full_name(self):
        return self.name_separator.join(str(node) for node in self.get_self_and_ancestors())

    @cached_property
    def full_path(self):
        return self.path_separator.join(node.slug for node in self.get_ancestors_and_self())


    def get_self_and_descendants(self):
        yield self
        for node in reversed(self.get_ancestors()):
            yield node


    def get_self_and_ancestors(self):
        yield self
        for node in reversed(self.get_ancestors()):
            yield node


    def get_ancestors_and_self(self):
        for node in self.get_ancestors():
            yield node
        yield self

    def get_descendants_and_self(self):
        for node in self.get_descendants():
            yield node
        yield self


class Category(SlugMixin, MP_Node, TreeNodeMixin):
    ''' The Category model, very straight forward. Includes a total_jobs
        method that returns the total of jobs with that category.
        The save() method is overriden so it can automatically asign
        a category order in case no one is provided.
    '''
    slug_field = 'name'

    name = models.CharField(_('Name'), unique=True, max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    category_order = models.PositiveIntegerField(_('Category order'), unique=True, blank=True, null=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['category_order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('djobberbase_category', kwargs={'categories': self.full_name, 'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.category_order:
            try:
                self.category_order = Category.objects.\
                                    latest('category_order').category_order + 1
            except Category.DoesNotExist:
                self.category_order = 0
        super(Category, self).save(*args, **kwargs)


class Type(SlugMixin, models.Model):
    ''' The Type model, nothing special, just the name and
        var_name fields. Again, the var_name is slugified by the overriden
        save() method in case it's not provided.
    '''
    slug_field = 'name'

    name = models.CharField(_('Name'), unique=True, max_length=255)

    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    def get_absolute_url(self):
        return reverse('djobberbase_type', kwargs={'type': self.slug})

    def __str__(self):
        return self.name


class Place(SlugMixin, MP_Node, TreeNodeMixin):
    ''' Place can be a country, state, county, place, street... and they can be nested.
    '''
    CONTINENT = 0   #Europe
    REGION = 1      #Central Europe
    COUNTRY = 2     #Germany
    STATE = 3       #Bavaria
    COUNTY = 4      #Oberpfalz
    CITY = 5        #Regensburg
    STREET = 6      #Silberne-Fisch-Gasse
    PLACE_TYPE_CHOICES = (
        (CONTINENT, _('Continent')),
        (REGION, _('Region')),
        (COUNTRY, _('Country')),
        (STATE, _('State')),
        (COUNTY, _('County')),
        (CITY, _('City')),
        (STREET, _('Street')),
    )

    slug_field = 'name'
    name_separator = ', '

    name = models.CharField(_('Name'), max_length=255)
    place_type = models.IntegerField(_('Place Type'), choices=PLACE_TYPE_CHOICES, default=CITY)


    def get_absolute_url(self):
        return reverse('djobberbase:category', kwargs={'categories': self.full_name, 'pk': self.pk})

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
        ordering = ['place_type']

    def __str__(self):
        return self.name


    #TODO does not work. It seems the ancestors are created after saving, so we cannot check them like this
    def clean(self):
        if self.place_type:
            ancestor = self.get_ancestors().filter(place_type__lte=self.place_type).aggregate(models.Max('place_type'))['place_type__max']
            if ancestor:
                possible_place_types = (place_type[1] for place_type in
                                        self.PLACE_TYPE_CHOICES[self.PLACE_TYPE_CHOICES.index(ancestor+1):])
                raise ValidationError(_('Place cannot be of this type. It needs to be one of: ')+str(possible_place_types))


    def save(self, *args, **kwargs):
        check_slug = not bool(self.slug)
        super(Place, self).save(*args, **kwargs)
        if check_slug:
            self.ensure_slug_uniqueness()


    def ensure_slug_uniqueness(self):
        """
        Ensures that the category's slug is unique amongst it's siblings.
        This is inefficient and probably not thread-safe.
        """
        self.slug = slugify(self.name)
        unique_slug = self.slug
        siblings = self.get_siblings().exclude(pk=self.pk)
        next_num = 2
        while siblings.filter(slug=unique_slug).exists():
            unique_slug = '{slug}-{end}'.format(slug=self.slug, end=next_num)
            next_num += 1

        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()


class Company(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, verbose_name=_('Company admin'), on_delete=models.CASCADE)
    logo = models.ImageField(verbose_name=_('Company logo'), upload_to='logos')

    def get_absolute_url(self):
        return reverse('djobberbase:company', self.admin.name)


class Education(SlugMixin, models.Model):
    slug_field = 'level'

    level = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.level


class Language(SlugMixin, models.Model):
    slug_field = 'name'

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Job(SlugMixin, models.Model):
    ''' The basic job model.
    '''
    slug_field = 'title'

    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.CASCADE, related_name='jobs')
    jobtype = models.ForeignKey(Type, verbose_name=_('Job Type'), on_delete=models.CASCADE, related_name='jobs')
    place = models.ForeignKey(Place, verbose_name=_('Place'), on_delete=models.CASCADE, related_name='jobs')
    education = models.ForeignKey(Education, blank=True, null=True)
    language = models.ForeignKey(Language, blank=True, null=True)

    company = models.ForeignKey(Company, verbose_name=_('Company'), on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    salary_range_min = models.PositiveIntegerField(verbose_name=_('Salary range minimum'), blank=True, null=True, db_index=True)
    salary_range_max = models.PositiveIntegerField(verbose_name=_('Salary range maximum'), blank=True, null=True)
    description = models.TextField(_('Description'))
    description_html = models.TextField(_('Description in HTML'), blank=True)
    url = models.URLField(_('External job URL'), blank=True, null=True)



    created_on = models.DateTimeField(_('Created on'), blank=True, default=timezone.now)
    valid_until = models.DateTimeField(_('Valid until'), blank=True, null=True)
    is_active = models.BooleanField(_('Created on'), default=True, db_index=True, help_text=_('You can hide the posting from others by unchecking this option.'))
    spotlight = models.BooleanField(_('Spotlight'), default=False, blank=True, db_index=True)

    objects = models.Manager()
    active = ActiveJobsManager()
    temporary = TempJobsManager()

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    @property
    def application_count(self):
        return self.stats.filter(stat_type=JobStat.APPLICATION).count()

    def switch_activate(self):
        self.is_active = not self.is_active
        self.save()


    def get_absolute_url(self):
        return ('djobberbase:job_detail', [self.user.name, self.title_slug])

    @property
    def activation_url(self):
        return ('djobberbase_job_activate', [self.id])

    @property
    def deactivation_url(self):
        return ('djobberbase_job_deactivate', [self.id])

    def clean(self):
        if self.valid_until:
            if self.valid_until < timezone.now():
                raise ValidationError(_("Job posting end date is in the past. "))

        slug = self.slug or self.get_slug(self.title)
        similar = self.__class__.active.filter(place=self.place, submitter=self.user, slug=slug)
        if similar:
            url = similar.get_absolute_url()
            raise ValidationError(_('Similar active job posting from your company already exists. You need to change the title of your posting or deactivate the original one. The original is available over here: ')+url)

    def save(self, *args, **kwargs):
        if self.salary_range_min:
            if not self.salary_range_max:
                self.salary_range_max = self.salary_range_min
        else:
            if self.salary_range_max:
                self.salary_range_min = self.salary_range_max

        if djobberbase_settings.DJOBBERBASE_MARKUP_LANGUAGE == 'textile':
            import textile
            self.description_html = mark_safe(
                                        force_text(
                                            textile.textile(
                                                smart_str(self.description))))
        #or markdown
        elif djobberbase_settings.DJOBBERBASE_MARKUP_LANGUAGE == 'markdown':
            import markdown
            self.description_html = mark_safe(
                                        force_text(
                                            markdown.markdown(
                                                smart_str(self.description))))
        else:
            self.description_html = self.description

        if djobberbase_settings.DJOBBERBASE_ENABLE_NEW_POST_MODERATION and self.is_active is None:
            self.is_active = False


        super().save(*args, **kwargs)


class JobStat(models.Model):
    APPLICATION = 'A'
    HIT = 'H'
    SPAM = 'S'
    STAT_TYPES = (
        (APPLICATION, _('Application')),
        (HIT, _('Hit')),
        (SPAM, _('Spam')),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='stats')
    created_on = models.DateTimeField(default=timezone.now, blank=True)
    stat_type = models.CharField(max_length=1, choices=STAT_TYPES, db_index=True, blank=True)
    description = models.TextField(_('Description'))
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = _('Job Stat')
        verbose_name_plural = _('Job Stats')
        ordering = ['-created_on']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self.stat_type == 'A':
            self.description = _('Job application for [{}]{} from IP: {}').format(self.job.pk, self.job.title)
        elif self.stat_type == 'H':
            self.description = _('Visit for [{}]{} from IP: {}').format(self.job.pk, self.job.title)
        elif self.stat_type == 'S':
            self.description = _('Spam report for [{}]{} from IP: {}').format(self.job.pk, self.job.title)
        else:
            self.description = _("Unkwown stat")
        super(JobStat, self).save(*args, **kwargs)


class JobSearch(models.Model):
    keywords = models.CharField(_('Keywords'), max_length=100, blank=False)
    created_on = models.DateTimeField(_('Created on'), default=timezone.now)

    class Meta:
        verbose_name = _('Search')
        verbose_name_plural = _('Searches')

    def __str__(self):
        return self.keywords