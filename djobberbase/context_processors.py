# -*- coding: utf-8 -*-

from djobberbase.conf import settings

def general_settings(request):
    return {setting:getattr(settings, setting) for setting in dir(settings) if setting.isupper()}