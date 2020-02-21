import warnings

from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig
from django.db import connection
from django.conf import settings


class BackendConfig(AppConfig):
    """ The backend app solely exists for triggering a backend signal. """
    name = 'backend'
    verbose_name = _('Backend')
