from distutils.version import StrictVersion
import re

import requests
from django.db.migrations.recorder import MigrationRecorder
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

