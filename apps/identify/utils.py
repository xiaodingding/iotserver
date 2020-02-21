# ~*~ coding: utf-8 ~*~
#
from __future__ import unicode_literals
import base64
import logging
import uuid

import requests
import ipaddress
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import authenticate, login as auth_login
from django.utils.translation import ugettext as _
from django.core.cache import cache

from common.tasks import send_mail_async
from common.utils import reverse, get_object_or_none
from users.models import User, LoginLog
from .models import Identify


logger = logging.getLogger('jumpserver')


def check_identify_valid(**kwargs):
    password = kwargs.pop('password', None)
    softid = kwargs.pop('softid', None)
    email = kwargs.pop('email', None)
    username = kwargs.pop('username', None)

    try:
        if username:
            user = get_object_or_none(User, username=username)
        elif email:
            user = get_object_or_none(User, email=email)
        else:
            user = None

        if user is None:
            return None, _('User not exist')
        elif not user.is_valid:
            return None, _('Disabled or expired')

        if password:
            realUser = authenticate(username=username, password=password)
            if not realUser:
                return None, _('Password or username(email)  invalid')
        else:
            return None, _('Password or username(email)  invalid')

        if softid:
            identify = Identify.objects.filter(user=realUser).filter(secret=softid)
            if identify :
                return realUser, ''
            else:
                return None, _('soft key invalid')
    except:
       pass
    return None, _('Password or soft key invalid')


def refresh_identify_token(token, user, expiration=settings.TOKEN_EXPIRATION or 3600):
    cache.set(token, user.id, expiration)


def generate_identify_token(request, user):
    expiration = settings.TOKEN_EXPIRATION or 3600
    remote_addr = request.META.get('REMOTE_ADDR', '')
    if not isinstance(remote_addr, bytes):
        remote_addr = remote_addr.encode("utf-8")
    remote_addr = base64.b16encode(remote_addr) #.replace(b'=', '')
    token = cache.get('%s_%s' % (user, remote_addr))
    if not token:
        token = uuid.uuid4().hex
        cache.set('%s_%s' % (user, remote_addr), token, expiration)
    return token

def validate_token(request, user):
    remote_addr = request.META.get('REMOTE_ADDR', '')
    if not isinstance(remote_addr, bytes):
        remote_addr = remote_addr.encode("utf-8")
    remote_addr = base64.b16encode(remote_addr) #.replace(b'=', '')
    token = cache.get('%s_%s' % (user, remote_addr))
    if not token:
        return None
    else:
        return token

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        pass
    return False


def write_login_log(username, type='', ip='', user_agent=''):
    msg = "username:{} type:{} ip:{} user_agent:{}".format(username, type, ip, user_agent)
    logger.debug(msg)
    if not (ip and validate_ip(ip)):
        ip = ip[:15]
        city = "Unknown"
    else:
        city = get_ip_city(ip)
    LoginLog.objects.create(
        username=username, type=type,
        ip=ip, city=city, user_agent=user_agent
    )


def get_ip_city(ip, timeout=10):
    # Taobao ip api: http://ip.taobao.com//service/getIpInfo.php?ip=8.8.8.8
    # Sina ip api: http://int.dpool.sina.com.cn/iplookup/iplookup.php?ip=8.8.8.8&format=json

    url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?ip=%s&format=json' % ip
    try:
        r = requests.get(url, timeout=timeout)
    except requests.Timeout:
        r = None
    city = 'Unknown'
    if r and r.status_code == 200:
        try:
            data = r.json()
            if not isinstance(data, int) and data['ret'] == 1:
                city = data['country'] + ' ' + data['city']
        except ValueError:
            pass
    return city
