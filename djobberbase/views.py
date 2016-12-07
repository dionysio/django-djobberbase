# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect
from djobberbase.models import Job, Category, Type, JobStat, JobSearch, Place, Company
from django.template.context_processors import csrf
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from djobberbase.helpers import *
from djobberbase.forms import ApplicationForm, SearchForm
from django.db.models import Count
from django.http import Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView


if djobberbase_settings.DJOBBERBASE_CAPTCHA_POST == 'simple':
    from djobberbase.forms import CaptchaJobForm
    _form_class = CaptchaJobForm
else:
    from djobberbase.forms import JobForm
    _form_class = JobForm


class ExtraContextMixin:
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class GenericJobListView(ExtraContextMixin, ListView):
    model = Job
    paginate_by = djobberbase_settings.DJOBBERBASE_JOBS_PER_PAGE
    extra_context = {"search_form": SearchForm(), "MEDIA_URL": settings.MEDIA_URL}

    def get_queryset(self):
        if self.kwargs.get('categories'):
            categories = self.kwargs['categories'].split('/')
            jobs = Job.active.filter(categories)
        else:
            jobs = Job.active.all().select_related('category', 'jobtype', 'place', 'company')


        return jobs

class JobListView(GenericJobListView):
    template_name = 'djobberbase/index.html'



class CityListView(ExtraContextMixin, ListView):
    model = Place
    extra_context = {'page_type': 'cities',
                     'other_cities_total': lambda: Job.active.filter(city=None).count()}


class JobCreateView(ExtraContextMixin, CreateView):
    model = Job
    form_class = _form_class

    def get_success_url(self):
        return reverse('djobberbase_job_verify', kwargs={"id": self.kwargs['job_id'], "auth": self.kwargs['auth']})


class JobDetail(ExtraContextMixin, DetailView):
    extra_context = {'page_type': 'detail',
                     'cv_extensions': djobberbase_settings.DJOBBERBASE_CV_EXTENSIONS,
                     'markup_lang': djobberbase_settings.DJOBBERBASE_MARKUP_LANGUAGE}

    template_name = 'djobberbase/job_detail.html'
    form_class = ApplicationForm

    def get_object(self, queryset=None):
        ''' Displays an active job and its application form depending if
            the job has online applications or not. Handles the job applications
            and sends notifications emails.
        '''
        try:
            job = Job.active.get(pk=self.kwargs['pk'])
        except Job.DoesNotExist: # Instead of throwing a 404 error redirect to job unavailable page
            return redirect('djobberbase_job_unavailable', permanent=True)

        #job.increment_view_count(self.request)
        ip = getIP(self.request)
        # Only if the job has online applications ON and application
        # notifications are activated can the user apply online
        mb = minutes_between()
        if job.apply_online and djobberbase_settings.DJOBBERBASE_APPLICATION_NOTIFICATIONS:
            self.extra_context.update(csrf(self.request))

            # If it's a job application
            if self.request.method == 'POST':

                # Gets the application
                form = ApplicationForm(self.request.POST,
                                       self.request.FILES,
                                       applicant_data={'ip': ip, 'mb': mb})

                # If the form is OK then send it to the job poster
                if form.is_valid():
                    application_mail = MailApplyOnline(job, self.request)
                    application_mail.start()

                    # Save JobStat application
                    ja = JobStat(job=job, ip=ip, stat_type=JobStat.APPLICATION)
                    ja.save()
                    messages.add_message(self.request,
                                         messages.INFO,
                                         _('Your application was sent successfully.'))
                    self.extra_context['page_type'] = 'application'
                    jobs = Job.active.filter(joburl=self.kwargs['joburl'])
                    return jobs
                else:
                    self.extra_context['form_error'] = True
            else:
                form = ApplicationForm(applicant_data={'ip': ip, 'mb': mb})
            self.extra_context['apform'] = form
            self.extra_context['object'] = job
            return job

        # Only display the job, without an application form
        else:
            self.extra_context['object'] = job
            return job


class JobVerify(DetailView):
    slug_url_kwarg = 'auth'
    slug_field = 'auth'
    extra_context = {'page_type': 'verify',
                     'markup_lang': djobberbase_settings.DJOBBERBASE_MARKUP_LANGUAGE}


class JobsCategory(ExtraContextMixin, ListView):
    paginate_by = djobberbase_settings.DJOBBERBASE_JOBS_PER_PAGE

    def get_queryset(self):
        jobs = Job.active.select_related('category', 'jobtype', 'place', 'company', 'company__admin')
        if self.kwargs.get('slug', None):
            category = get_object_or_404(Category, slug=self.kwargs['slug'])
            queryset = jobs.filter(category=category)
            self.extra_context['selected_category'] = category
        if self.kwargs.get('job_type', None):
            jobtype = get_object_or_404(Type, slug=self.kwargs['job_type'])
            jobs = queryset.filter(jobtype=jobtype)
            self.extra_context['selected_jobtype'] = jobtype
        return jobs

class JobsCompany(ExtraContextMixin, ListView):
    paginate_by = djobberbase_settings.DJOBBERBASE_JOBS_PER_PAGE

    def get_queryset(self):
        company = get_object_or_404(Company, admin__username=self.kwargs['company'])
        return company.jobs.select_related('category', 'jobtype', 'place', 'company', 'company__admin')

class JobsInCity(ExtraContextMixin, ListView):
    paginate_by = djobberbase_settings.DJOBBERBASE_JOBS_PER_PAGE

    def get_queryset(self):
        city = get_object_or_404(Place, ascii_name=self.kwargs['city_name'])
        jobs = Job.active.filter(city=city)
        self.extra_context = {'place': city}
        if self.kwargs.get('tvar_name', None):
            jobtype = get_object_or_404(Type, var_name=self.kwargs['tvar_name'])
            jobs = jobs.filter(jobtype=jobtype)
            self.extra_context['selected_jobtype'] = jobtype
        return jobs


class JobsOtherCities(ListView):
    def get_queryset(self):
        return Job.active.filter(city=None)


class Companies(ListView):
    template_name = 'djobberbase/company_list.html'

    def get_queryset(self):
        return Job.active.values('company', 'company_slug').annotate(Count('company'))


class JobsAt(ExtraContextMixin, ListView):
    model = Job
    def get_queryset(self):
        jobs = Job.active.filter(company_slug=self.kwargs['company_slug'])
        if self.kwargs.get('tvar_name', None):
            jobtype = get_object_or_404(Type, var_name=self.kwargs['company_slug'])
            jobs = jobs.filter(jobtype=jobtype)
            self.extra_context['selected_jobtype'] = jobtype
        return jobs


def job_confirm(request, job_id, auth):
    ''' A view to confirm a recently created job, if it has been published
        by a previously approved user then it gets automatically published,
        if not then it will need to be verified by a moderator.
    '''
    job = get_object_or_404(Job, pk=job_id, auth=auth)
    if job.status not in (Job.ACTIVE, Job.TEMPORARY):
        raise Http404
    new_post = job.is_temporary()
    requires_mod = not job.email_published_before and \
                 djobberbase_settings.DJOBBERBASE_ENABLE_NEW_POST_MODERATION
    if requires_mod:
        messages.add_message(request, 
                       messages.INFO, 
                       _('Your job post needs to be verified by a moderator.'))
        if djobberbase_settings.DJOBBERBASE_POSTER_NOTIFICATIONS:
            pending_email = MailPublishPendingToUser(job, request)
            pending_email.start()
    else:
        messages.add_message(request, 
                             messages.INFO, 
                             _('Your job post has been published.'))
        if not job.is_active():
            job.activate()
        if new_post:
            if djobberbase_settings.DJOBBERBASE_POSTER_NOTIFICATIONS:
                publish_email = MailPublishToUser(job, request)
                publish_email.start()    
    queryset = Job.objects.all()
    if djobberbase_settings.DJOBBERBASE_ADMIN_NOTIFICATIONS:
        admin_email = MailPublishToAdmin(job, request)
        admin_email.start()
    return object_detail(request, queryset=queryset,
                         object_id=job_id,
                         extra_context={'page_type':'confirm'})


class GenericJobUpdateView(ExtraContextMixin, UpdateView):
    model = Job

    def get_object(self, queryset=None):
        return get_object_or_404(Job, pk=self.kwargs['job_id'], auth=self.kwargs['auth'])


class JobUpdateView(GenericJobUpdateView):
    form_class = JobForm

    def get_success_url(self):
        return '../../../{}/%(id)d/%(auth)s/'.format(djobberbase_settings.DJOBBERBASE_VERIFY_URL)

    def get_object(self, queryset=None):
        job = super().get_object(queryset=queryset)
        if not job.is_active and not job.is_temporary:
            raise Http404
        return job


class JobActivate(GenericJobUpdateView):
    def get_object(self, queryset=None):
        ''' Gets a job and activates it, only if it's not already activated,
            it also sends the notification mail to the poster.
        '''
        job = super().get_object(queryset=queryset)
        if not job.is_active:
            job.activate()
            if djobberbase_settings.DJOBBERBASE_POSTER_NOTIFICATIONS:
                publish_email = MailPublishToUser(job, self.request)
                publish_email.start()
            messages.add_message(self.request, messages.INFO,
                                 _('Your job has been activated.'))
            self.extra_context['page_type'] = 'activate'
        return job


class JobDeactivate(GenericJobUpdateView):

    def get_success_url(self):
        return redirect('')

    def get_object(self, queryset=None):
        ''' Deactivates a job and shows an active jobs list.
        '''
        job = super().get_object(queryset=queryset)
        if job.is_active or job.is_temporary:
            job.deactivate()
            messages.add_message(self.request,
                                 messages.INFO,
                                 _('Your job has been deactivated.'))
            self.extra_context['page_type'] = 'deactivate'
        return job


class JobSearchView(GenericJobListView):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        found_entries = Job.objects.none()
        self.extra_context = {'keywords': ' '}
        if ('keywords' in self.request.GET) and self.request.GET['keywords'].strip():
            query_string = self.request.GET['keywords']
            place = self.request.GET.get('place', '')
            self.extra_context['keywords'] = query_string
            entry_query = get_query(query_string, search_fields=['title', 'description', 'category',
                             'jobtype', ])
            found_entries = Job.objects.filter(entry_query)
            if place:
                found_entries.filter(place__name=place)
            found_entries = found_entries.select_related('category', 'jobtype', 'place', 'company', 'company__admin').order_by('-created_on')[:djobberbase_settings.DJOBBERBASE_JOBS_PER_SEARCH]
            #self.extra_context['length'] = found_entries.count()
            #JobSearch.objects.create(keywords=query_string)
        return found_entries