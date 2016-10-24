#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json

from django.db import transaction
from django.core.management.base import BaseCommand
from django.utils import timezone

from djobberbase.models import Job
from django.utils.translation import ugettext_lazy as _

class Command(BaseCommand):
    help = _('Cleans up old jobs which are past their validity date.')

    def add_arguments(self, parser):
        parser.add_argument('--force', '-f', dest='force', default=False)

    def handle(*args, **kwargs):
        cleanup = Job.objects.filter(is_active=True, valid_until__lte=timezone.now())
        if cleanup:
            agree = kwargs.get('force')
            if not agree:
                agree = input(_("This action will mark {} jobs as inactive. Do you agree? y/n").format(cleanup.count()))
                agree = agree == 'y'
            if agree:
                cleanup.update(is_active=True)