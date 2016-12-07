# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from djobberbase.models import Category, Type, Job, Place, JobStat, JobSearch, Company

def activate_jobs(modeladmin, request, queryset):
    queryset.update(status=Job.ACTIVE)
activate_jobs.short_description = _('Activate selected jobs.')


def deactivate_jobs(modeladmin, request, queryset):
    queryset.update(status=Job.INACTIVE)
deactivate_jobs.short_description = _('Deactivate selected jobs.')


def mark_spotlight(modeladmin, request, queryset):
    queryset.update(spotlight=True)
mark_spotlight.short_description = _('Mark selected jobs as spotlight.')


class JobAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Job Details'), {'fields': ['jobtype', 'category', 'title', \
                                    'place', 'description']}),
        (_('Company Info'), {'fields': ['company', 'url', ]}),
        (_('Admin Info'),  {'fields': ['spotlight']}),
    ]
    list_display = ('title', 'company', 'created_on', 'get_status_with_icon', 'spotlight')
    actions = [activate_jobs, deactivate_jobs, mark_spotlight]

    def get_status_with_icon(self, obj):
        image = 'icon-yes.gif'

        admin_media = settings.STATIC_URL
        icon = '<img src="%(admin_media)sadmin/img/%(image)s" alt="%(status)s" /> %(status)s'


        return icon % {'admin_media': admin_media,
                       'image': image,
                       'status': ''}
    get_status_with_icon.allow_tags = True
    get_status_with_icon.admin_order_field = 'status'
    get_status_with_icon.short_description = 'Status'


class CategoryAdmin(TreeAdmin):
    list_per_page = 25
    list_display = ('name', 'description', 'depth', 'category_order', 'full_name')
    form = movenodeform_factory(Category)
    search_fields = ('name', 'description')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('logo', 'admin', )
    search_fields = ('admin__email', )

class PlaceAdmin(TreeAdmin):
    form = movenodeform_factory(Place)
    list_per_page = 25
    list_display = ('name', 'place_type', 'depth', 'reversed_full_name')
    list_filter = ('place_type', )
    search_fields = ('name', )



class JobStatAdmin(admin.ModelAdmin):
    readonly_fields = ['description', 'job', 'created_on', 'ip', 'stat_type']


class JobSearchAdmin(admin.ModelAdmin):
    readonly_fields = ['keywords', 'created_on']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
"""
admin.site.register(JobStat, JobStatAdmin)
admin.site.register(JobSearch, JobSearchAdmin)"""
