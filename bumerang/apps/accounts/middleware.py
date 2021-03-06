# -*- coding: utf-8 -*-
from django.conf import settings
#import bumerang.settings as settings
from datetime import timedelta, date


class KeepLoggedInMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated() or not settings.KEEP_LOGGED_KEY in request.session:
            return
        if request.session[settings.KEEP_LOGGED_KEY] != date.today():
            request.session.set_expiry(timedelta(days=settings.KEEP_LOGGED_DURATION))
            request.session[settings.KEEP_LOGGED_KEY] = date.today()
        return
