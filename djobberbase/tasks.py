#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core import mail
from django.conf import settings


if settings.DJOBBERBASE_ASYNC_NOTIFICATIONS:
    from celery import shared_task

    @shared_task
    def send_mail(*args, **kwargs):
        return mail.send_mail(*args, **kwargs)
else:
    send_mail = mail.send_mail
