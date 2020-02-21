# -*- coding: utf-8 -*-
#

from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

from common.utils import get_logger


logger = get_logger(__file__)


