# -*- coding: utf-8 -*-
import django
if django.get_version() >= '1.6':
    from django.conf.urls import patterns, url, include
else:
    from django.conf.urls.defaults import *
from djobberbase.models import Job, Category, Type, City
from djobberbase.conf import settings as djobberbase_settings
from djobberbase.feeds import LatestJobsFeed
from djobberbase.views import JobListView, CityListView

if djobberbase_settings.DJOBBERBASE_CAPTCHA_POST == 'simple':
    from djobberbase.forms import CaptchaJobForm
    form_class = CaptchaJobForm
else:
    from djobberbase.forms import JobForm
    form_class = JobForm

urlpatterns = patterns('',
    #An index view
    url(r'^$', JobListView.as_view(), name='djobberbase_job_list'),
    url(r'^'+djobberbase_settings.DJOBBERBASE_CITIES_URL+'/$', 
        CityListView.as_view(), name='djobberbase_cities_list'),
    url(r'^cities-list', JobListView.as_view(), name='djobberbase_cities_list'),
    url(r'^job-post', JobListView.as_view(), name='djobberbase_job_post'),
    url(r'^job-un', JobListView.as_view(), name='djobberbase_job_unavailable'),
    #verify job
    url(r'^'+djobberbase_settings.DJOBBERBASE_VERIFY_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'djobberbase.views.job_verify', 
        name='djobberbase_job_verify'),

    #all jobs
    url(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_URL+'/$',
        'djobberbase.views.jobs_category',
        name='djobberbase_job_list_all'),

    #all jobs with category
    url(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_URL+
        '/(?P<cvar_name>[-\w]+)/$',
        'djobberbase.views.jobs_category',
        name='djobberbase_job_list_category'),

    #all jobs with category and job type    
    url(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_URL+
        '/(?P<cvar_name>[-\w]+)/(?P<tvar_name>[-\w]+)/$',
        'djobberbase.views.jobs_category',
        name='djobberbase_job_list_category_type'),

    #Job detail    
    url(r'^'+djobberbase_settings.DJOBBERBASE_JOB_URL+
        '/(?P<job_id>\d+)/(?P<joburl>[-\w]+)/$',
        'djobberbase.views.job_detail',
        name='djobberbase_job_detail'),
        
    #Jobs in city view
    url(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_IN_URL+
        '/(?P<city_name>[-\w]+)/$',
        'djobberbase.views.jobs_in_city',
        name='djobberbase_jobs_in_city'),

    #Jobs in other cities
    url(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_IN_OTHER_CITIES+'/$',
        'djobberbase.views.jobs_in_other_cities',
        name='djobberbase_jobs_in_other_cities'),

    #Jobs in city+jobtype view
    url(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_IN_URL+
        '/(?P<city_name>[-\w]+)/(?P<tvar_name>[-\w]+)/$',
        'djobberbase.views.jobs_in_city',
        name='djobberbase_jobs_in_city_jobtype'),

    #Companies
    url(r'^'+djobberbase_settings.DJOBBERBASE_COMPANIES_URL+'/$',
        'djobberbase.views.companies',
        name='djobberbase_companies'),

    #Jobs at (company)
    url(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_AT_URL+
        '/(?P<company_slug>[-\w]+)/$',
        'djobberbase.views.jobs_at',
        name='djobberbase_jobs_at'),

    #Job confirm
    url(r'^'+djobberbase_settings.DJOBBERBASE_CONFIRM_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'djobberbase.views.job_confirm',
        name='djobberbase_job_confirm'),

    #Edit job
    url(r'^'+djobberbase_settings.DJOBBERBASE_POST_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'djobberbase.views.job_edit',
        name='djobberbase_job_edit'),

    #Activate job
    url(r'^'+djobberbase_settings.DJOBBERBASE_ACTIVATE_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'djobberbase.views.job_activate',
        name='djobberbase_job_activate'),

    #Deactivate job
    url(r'^'+djobberbase_settings.DJOBBERBASE_DEACTIVATE_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'djobberbase.views.job_deactivate',
        name='djobberbase_job_deactivate'),

    #Search
    url(r'^'+djobberbase_settings.DJOBBERBASE_SEARCH_URL+'/$',
        'djobberbase.views.job_search',
        name='djobberbase_job_search'),

    #Feed
    url(r'^rss/(?P<var_name>[-\w]+)/$',
        LatestJobsFeed(),
        name='djobberbase_feed'),

)
