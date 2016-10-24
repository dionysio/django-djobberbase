# -*- coding: utf-8 -*-
from time import time
import threading

from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.forms import model_to_dict
from django.template.loader import render_to_string

from djobberbase.helpers import getIP, handle_uploaded_file, delete_uploaded_file
from djobberbase.conf import settings as djobberbase_settings
from djobberbase import tasks

site_domain = Site.objects.get_current().domain
site_url = lambda url, domain=site_domain, protocol="http": "{}://{}{}".format(protocol, domain, url)


def mail_template(job, email_template, subject_string, to, msg='', from_email=djobberbase_settings.DJOBBERBASE_ADMIN_EMAIL, include_activate_url=False):
    context = model_to_dict(job, fields=('url', 'title', 'company', 'description', 'poster_email', 'post_date'))
    context['job_url'] = site_url(job.absolute_url)
    context['job_edit_url'] = site_url(job.edit_url)
    context['job_deactivate_url'] = site_url(job.deactivation_url)
    context['msg_body'] = msg

    job_info = {
        'site_name': djobberbase_settings.DJOBBERBASE_SITE_NAME,
        'job_title': job.title,
    }
    subject = subject_string % job_info
    if include_activate_url and not job.is_active:
        subject = djobberbase_settings.DJOBBERBASE_NEW_POST_ADMIN_SUBJECT % job_info
        context['job_activate_url'] = site_url(job.activation_url)

    text_content = render_to_string('djobberbase/emails/{}.txt'.format(email_template), context)
    html_content = render_to_string('djobberbase/emails/{}.html'.format(email_template), context)
    return tasks.send_mail(subject=subject, body=text_content, from_email=from_email, to=[to], html_message=html_content)


def mail_publish_to_admin(job):
    return mail_template(job, email_template='publish_to_admin', to=djobberbase_settings.DJOBBERBASE_ADMIN_EMAIL,
                         subject_string=djobberbase_settings.DJOBBERBASE_EDIT_POST_ADMIN_SUBJECT, include_activate_url=True)


def mail_publish_pending_to_user(job):
    return mail_template(job, email_template='publish_pending_to_user', to=job.poster_email,
                         subject_string=djobberbase_settings.DJOBBERBASE_MAIL_PENDING_SUBJECT)


def mail_publish_to_user(job):
    return mail_template(job, email_template='publish_to_user', to=job.poster_email,
                         subject_string=djobberbase_settings.DJOBBERBASE_MAIL_PUBLISH_SUBJECT)


def mail_apply_online(job, **post_args):
    return mail_template(job, email_template='publish_to_user', to=job.poster_email,
                         subject_string=djobberbase_settings.DJOBBERBASE_MAIL_APPLY_ONLINE_SUBJECT)

class MailApplyOnline(threading.Thread):

    def __init__(self, job, request):
        threading.Thread.__init__(self)
        job_info = {
                    'site_name': djobberbase_settings.DJOBBERBASE_SITE_NAME,
                    'job_title': job.title,
        }
        subject = djobberbase_settings.DJOBBERBASE_MAIL_APPLY_ONLINE_SUBJECT % job_info
        from_email = djobberbase_settings.DJOBBERBASE_ADMIN_EMAIL
        to = job.poster_email
        msg = request.POST['apply_msg']
        self.email = EmailMessage(subject, msg, from_email, [to], headers = {'Reply-To': request.POST['apply_email']})
        if 'apply_cv' in request.FILES.keys():
            name = "{}_{}".format(int(time()), request.FILES['apply_csv'].name)
            handle_uploaded_file(request.FILES['apply_cv'], name)
            self.email.attach_file(djobberbase_settings.DJOBBERBASE_FILE_UPLOADS + name)
            delete_uploaded_file(djobberbase_settings.DJOBBERBASE_FILE_UPLOADS + name)