# -*- coding: utf-8 -*-
from django.conf.urls import url

from djobberbase.conf import settings as djobberbase_settings
from djobberbase.feeds import LatestJobsFeed
from djobberbase import views

appname = 'djobberbase'
urlpatterns = (
    url(r'^$', views.JobListView.as_view(), name='index'),
    url(r'^job-un', views.JobListView.as_view(), name='job_unavailable'),
    url(r'^{}/employer/(?P<company>\w+)/$'.format(djobberbase_settings.DJOBBERBASE_JOBS_URL),
        views.JobsCompany.as_view(),
        name='company_jobs'),
    url(r'^{}/(?:(?P<slug>[-\w]*)/)?(?:(?P<job_type>[-\w]*)/)?$'.format(
        djobberbase_settings.DJOBBERBASE_JOBS_URL),
        views.JobsCategory.as_view(),
        name='category'),
    url(r'^{}/(?P<company>\w+)/(?P<title_slug>[-\w]+)~(?P<pk>\d+)/$'.format(djobberbase_settings.DJOBBERBASE_JOB_URL),
        views.JobDetail.as_view(),
        name='job_detail'),
    url(r'^{}/(?:(?P<categories>[-\w]*)/)?(?:(?P<jobtype>[-\w]*)/)?$'.format(djobberbase_settings.DJOBBERBASE_JOBS_URL),
        views.JobsCategory.as_view(),
        name='job_list_all'),

    url(r'^{}/$'.format(djobberbase_settings.DJOBBERBASE_SEARCH_URL),
        views.JobSearchView.as_view(),
        name='job_search'),
    url(r'^job-post', views.JobCreateView.as_view(), name='job_post'),
    url(r'^job-post', views.JobCreateView.as_view(), name='job_post'),
    url(r'^rss/(?P<var_name>[-\w]+)/$', LatestJobsFeed(), name='feed'),
)
"""
urlpatterns = (#An index view

    url(r'^{}/$'.format(djobberbase_settings.DJOBBERBASE_CITIES_URL),
        views.CityListView.as_view(), name='cities_list'),
    url(r'^cities-list', views.CityListView.as_view(), name='cities_list'),


    #verify job
    url(r'^{}/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$'.format(djobberbase_settings.DJOBBERBASE_VERIFY_URL),
        views.JobVerify.as_view(),
        name='job_verify'),


    url(r'^{}/(?:(?P<cvar_name>[-\w]*)/)?(?:(?P<tvar_name>[-\w]*)/)?$'.format(djobberbase_settings.DJOBBERBASE_JOBS_URL),
        views.JobsCategory.as_view(),
        name='job_list_all'),

    url(r'^{}/(?:(?P<categories>[-\/a-zA-Z]*)~(?P<pk>[\d]*)/)?(?:(?P<job_type>[-\w]*)/)?$'.format(
        djobberbase_settings.DJOBBERBASE_JOBS_URL),
        views.JobsCategory.as_view(),
        name='category'),

    #Job detail    
    url(r'^{}/(?P<company>\w+)/(?P<title_slug>[-\w]+)~(?P<pk>\d+)/$'.format(djobberbase_settings.DJOBBERBASE_JOB_URL),
        views.JobDetail.as_view(),
        name='job_detail'),
        
    #Jobs in place view
    url(r'^{}/(?P<city_name>[-\w]+)/$'.format(djobberbase_settings.DJOBBERBASE_JOBS_IN_URL),
        views.JobsInCity.as_view(),
        name='jobs_in_city'),

    #Jobs in other cities
    url(r'^{}/$'.format(djobberbase_settings.DJOBBERBASE_JOBS_IN_OTHER_CITIES),
        views.JobsOtherCities.as_view(),
        name='jobs_in_other_cities'),

    #Jobs in place+jobtype view
    url(r'^{}/(?P<city_name>[-\w]*)/(?P<tvar_name>[-\w]*)/$'.format(djobberbase_settings.DJOBBERBASE_JOBS_IN_URL),
        views.JobsInCity.as_view(),
        name='jobs_in_city_jobtype'),

    #Companies
    url(r'^{}/$'.format(djobberbase_settings.DJOBBERBASE_COMPANIES_URL),
        views.Companies.as_view(),
        name='companies'),

    #Jobs at (company)
    url(r'^{}/(?:(?P<company_slug>[-\w]*)/)?$'.format(djobberbase_settings.DJOBBERBASE_JOBS_AT_URL),
        views.JobsAt.as_view(),
        name='jobs_at'),

    #Job confirm
    url(r'^{}/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$'.format(djobberbase_settings.DJOBBERBASE_CONFIRM_URL),
        views.job_confirm,
        name='job_confirm'),

    #Edit job
    url(r'^{}/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$'.format(djobberbase_settings.DJOBBERBASE_POST_URL),
        views.JobUpdateView.as_view(),
        name='job_edit'),

    #Activate job
    url(r'^{}/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$'.format(djobberbase_settings.DJOBBERBASE_ACTIVATE_URL),
        views.JobActivate.as_view(),
        name='job_activate'),

    #Deactivate job
    url(r'^{}/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$'.format(djobberbase_settings.DJOBBERBASE_DEACTIVATE_URL),
        views.JobDeactivate.as_view(),
        name='job_deactivate'),

    #Search
    url(r'^{}/$'.format(djobberbase_settings.DJOBBERBASE_SEARCH_URL),
        views.JobSearchView.as_view(),
        name='job_search'),

    #Feed
    url(r'^rss/(?P<var_name>[-\w]+)/$',
        LatestJobsFeed(),
        name='feed'),

)"""