# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# General settings
DJOBBERBASE_SITE_NAME = getattr(settings, 'DJOBBERBASE_SITE_NAME', 'Djobberbase')
DJOBBERBASE_HTML_TITLE = getattr(settings, 'DJOBBERBASE_HTML_TITLE', 'Djobberbase :: A jobberBase clone written using the Django framework')
DJOBBERBASE_SITE_DESCRIPTION = getattr(settings, 'DJOBBERBASE_SITE_DESCRIPTION', 'Djobberbase jobs.')
DJOBBERBASE_MINUTES_BETWEEN = getattr(settings, 'DJOBBERBASE_MINUTES_BETWEEN', 10)
DJOBBERBASE_DEFAULT_PLACE_HIERARCHY = getattr(settings, 'DJOBBERBASE_DEFAULT_PLACE_HIERARCHY', 4)
DJOBBERBASE_MAX_UPLOAD_SIZE = getattr(settings, 'DJOBBERBASE_MAX_UPLOAD_SIZE', 3145728)
DJOBBERBASE_FILE_UPLOADS = getattr(settings, 'DJOBBERBASE_FILE_UPLOADS', './uploads/')
DJOBBERBASE_JOBS_PER_PAGE = getattr(settings, 'DJOBBERBASE_JOBS_PER_PAGE', 50)
DJOBBERBASE_JOBS_PER_SEARCH = getattr(settings, 'DJOBBERBASE_JOBS_PER_SEARCH', 25)
DJOBBERBASE_MAX_VISITS_PER_HOUR = getattr(settings, 'DJOBBERBASE_MAX_VISITS_PER_HOUR', 1)
DJOBBERBASE_CAPTCHA_POST = getattr(settings, 'DJOBBERBASE_CAPTCHA_POST', None)
DJOBBERBASE_CAPTCHA_APPLICATION = getattr(settings, 'DJOBBERBASE_CAPTCHA_APPLICATION', None)
DJOBBERBASE_CV_EXTENSIONS = getattr(settings, 'DJOBBERBASE_CV_EXTENSIONS', ('pdf', 'rtf', 'doc', 'docx', 'odt'))

DJOBBERBASE_POST_URL = getattr(settings, 'DJOBBERBASE_POST_URL', 'post')
DJOBBERBASE_VERIFY_URL = getattr(settings, 'DJOBBERBASE_VERIFY_URL', 'verify')
DJOBBERBASE_CONFIRM_URL = getattr(settings, 'DJOBBERBASE_CONFIRM_URL', 'confirm')
DJOBBERBASE_JOB_URL = getattr(settings, 'DJOBBERBASE_JOB_URL', 'job')
DJOBBERBASE_AT_URL = getattr(settings, 'DJOBBERBASE_AT_URL', 'at')
DJOBBERBASE_JOBS_URL = getattr(settings, 'DJOBBERBASE_JOBS_URL', 'jobs')
DJOBBERBASE_CITIES_URL = getattr(settings, 'DJOBBERBASE_CITIES_URL', 'cities')
DJOBBERBASE_COMPANIES_URL = getattr(settings, 'DJOBBERBASE_COMPANIES_URL', 'companies')
DJOBBERBASE_JOBS_IN_URL = getattr(settings, 'DJOBBERBASE_JOBS_IN_URL', 'jobs-in')
DJOBBERBASE_JOBS_IN_OTHER_CITIES = getattr(settings, 'DJOBBERBASE_JOBS_IN_OTHER_CITIES', 'jobs-in-other-cities')
DJOBBERBASE_JOBS_AT_URL = getattr(settings, 'DJOBBERBASE_JOBS_AT_URL', 'jobs-at')
DJOBBERBASE_ACTIVATE_URL = getattr(settings, 'DJOBBERBASE_ACTIVATE_URL', 'activate')
DJOBBERBASE_DEACTIVATE_URL = getattr(settings, 'DJOBBERBASE_DEACTIVATE_URL', 'deactivate')
DJOBBERBASE_SEARCH_URL = getattr(settings, 'DJOBBERBASE_SEARCH_URL', 'search')
DJOBBERBASE_UNAVAILABLE_URL = getattr(settings, 'DJOBBERBASE_UNAVAILABLE_URL', 'job-unavailable')

# Mailing settings
DJOBBERBASE_ASYNC_NOTIFICATIONS = getattr(settings, 'DJOBBERBASE_ASYNC_NOTIFICATIONS', False)
DJOBBERBASE_ENABLE_NEW_POST_MODERATION = getattr(settings, 'DJOBBERBASE_ENABLE_NEW_POST_MODERATION', True)

DJOBBERBASE_ADMIN_EMAIL = getattr(settings, 'DJOBBERBASE_ADMIN_EMAIL', '')
DJOBBERBASE_ADMIN_NOTIFICATIONS = getattr(settings, 'DJOBBERBASE_ADMIN_NOTIFICATIONS', False)
DJOBBERBASE_POSTER_NOTIFICATIONS = getattr(settings, 'DJOBBERBASE_POSTER_NOTIFICATIONS', False)
DJOBBERBASE_APPLICATION_NOTIFICATIONS = getattr(settings, 'DJOBBERBASE_APPLICATION_NOTIFICATIONS', False)

DJOBBERBASE_NEW_POST_ADMIN_SUBJECT = getattr(settings, 
                                    'DJOBBERBASE_NEW_POST_ADMIN_SUBJECT', 
                                    _('[ %(site_name)s  ] New job: %(job_title)s'))

DJOBBERBASE_EDIT_POST_ADMIN_SUBJECT = getattr(settings, 
                                    'DJOBBERBASE_EDIT_POST_ADMIN_SUBJECT', 
                                    _('[ %(site_name)s  ] Edited job: %(job_title)s'))

DJOBBERBASE_MAIL_PENDING_SUBJECT = getattr(settings, 
                                    'DJOBBERBASE_MAIL_PENDING_SUBJECT', 
                                    _('Your ad on %(site_name)s'))

DJOBBERBASE_MAIL_PUBLISH_SUBJECT = getattr(settings, 
                                    'DJOBBERBASE_MAIL_PUBLISH_SUBJECT', 
                                    _('Your ad on %(site_name)s was published'))
 
DJOBBERBASE_MAIL_APPLY_ONLINE_SUBJECT = getattr(settings, 
                                    'DJOBBERBASE_MAIL_APPLY_ONLINE_SUBJECT', 
                                    _('[ %(site_name)s ] I wish to apply for %(job_title)s'))


# Markup settings
DJOBBERBASE_MARKUP_LANGUAGE = getattr(settings, 'DJOBBERBASE_MARKUP_LANGUAGE', None) #options: 'textile', 'markdown'

