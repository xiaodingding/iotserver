# ~*~ coding: utf-8 ~*~

# Copyright (C) 2014-2017 Beijing DuiZhan Technology Co.,Ltd. All Rights Reserved.
#
# Licensed under the GNU General Public License v2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.gnu.org/licenses/gpl-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import OrderedDict
import copy
import logging
import os
import random
import uuid
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from rest_framework import generics
from rest_framework.response import Response
from rest_framework_bulk import BulkModelViewSet
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from rest_framework import viewsets, serializers
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404

from common.mixins import CustomFilterMixin
from common.utils import get_object_or_none

from .hands import IsAppUser, IsSuperUser, IsValidUser, IsSuperUserOrAppUser
from django.core.cache import cache
from django.utils import timezone

from .models.device import Device
from .models.datatemplet import DataTemplet
from .models.datapoint import DataPoint
from .models.group import DeviceGroup
from .models.data import Data

from . import serializers
from .utils import device_point_query

from common.utils import get_logger

logger = get_logger(__file__)

class DeviceUpdateAssetsApi(generics.RetrieveUpdateAPIView):
    """Device update asset member"""
    queryset = Device.objects.all()
    #serializer_class = serializers.DeviceUpdateSerializer
    permission_classes = (IsSuperUserOrAppUser,)


class DeviceViewSet(CustomFilterMixin, BulkModelViewSet):
    """Device api set, for add,delete,update,list,retrieve resource"""
    queryset = Device.objects.all()
    serializer_class = serializers.DeviceSerializer
    permission_classes = (IsSuperUserOrAppUser,)

    def get_queryset(self):
        queryset = super(DeviceViewSet, self).get_queryset()
        # print(self.request.user.is_superuser)
        if self.request.user.is_superuser:
            #queryset = queryset.filter(is_deleted=False)
            pass
        else:
            queryset = queryset.filter(is_deleted=True)
        device_id = self.request.query_params.get('device_id', '')
        # system_users_id = self.request.query_params.get('system_user_id', '')
        device_group_id = self.request.query_params.get('device_group_id', '')
        # admin_user_id = self.request.query_params.get('admin_user_id', '')
        if device_id:
            queryset = queryset.filter(device__sn=device_id)
        if device_group_id:
            queryset = queryset.filter(groups__id=device_group_id)
        return queryset


class DeviceGroupViewSet(CustomFilterMixin, BulkModelViewSet):
    """Asset group api set, for add,delete,update,list,retrieve resource"""
    queryset = DeviceGroup.objects.all()
    serializer_class = serializers.DeviceGroupSerializer
    permission_classes = (IsSuperUser,)


class DataTpViewSet(CustomFilterMixin, BulkModelViewSet):
    """Asset group api set, for add,delete,update,list,retrieve resource"""
    queryset = DataTemplet.objects.all()
    serializer_class = serializers.DataTpSerializer
    permission_classes = (IsSuperUserOrAppUser,)



class DataPointViewSet(CustomFilterMixin, BulkModelViewSet):
    """Asset group api set, for add,delete,update,list,retrieve resource"""
    queryset = DataPoint.objects.all()
    serializer_class = serializers.DataPointSerializer
    permission_classes = (IsSuperUserOrAppUser,)



class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = serializers.DataSerializer
    permission_classes = (IsSuperUserOrAppUser,)


def DataHistoryView(request):
    if request.method == 'GET':
        device_id = request.GET.get('device_id')
        if not device_id:
            return HttpResponse('device_id is not valid', status=400)
        else:
            jsondata="["
            device = Device.objects.filter(id=device_id).all()[:1]
            if not device:
                return HttpResponse("not find", status=404)
            device = device[0]
            dtpoint = device_point_query(device)
            templet = device.datatemplet.all()[:1]

            # print("device:%s, templet: %s, dtpoint:%s %d" % (device, templet, dtpoint, len(dtpoint)))
            if (templet is None  or dtpoint is None):
                return HttpResponse("not find data templet and not find datapoint", status=404)
            else:
                data_que = Data.objects.filter(device=device)
                j = 0
                for ht in data_que:
                    history = "["
                    data = ht.data_content.split(";")
                    history = history + "\"" + ht.date_created.strftime("%H:%M:%S") + "\""

                    if (len(data) < len(dtpoint)):
                        for i in range(len(data), (len(dtpoint))):
                            data.append('0')
                    i = 0
                    for key in dtpoint:
                        history = history + "," +data[i]
                        i = i +1
                    history = history + "]"
                    print("history: %s" % history)

                    if j > 0:
                        jsondata = jsondata + "," + history
                    else:
                        jsondata = jsondata + history
                    j = j + 1
                jsondata = jsondata + "]"
                print(jsondata)

                return HttpResponse(jsondata, status=200)



def DataLatestView(request):
    if request.method == 'GET':
        device_id = request.GET.get('device_id')
        if not device_id:
            return HttpResponse('device_id is not valid', status=400)
        else:
            jsondata="["

            device = Device.objects.filter(id=device_id).all()[:1]
            if not device:
                return HttpResponse("not find", status=404)
            device = device[0]
            dtpoint = device_point_query(device)
            templet = device.datatemplet.all()[:1]

            # print("device:%s, templet: %s, dtpoint:%s %d" % (device, templet, dtpoint, len(dtpoint)))
            if (templet is None  or dtpoint is None):
                return HttpResponse("not find templet or datapoint", status=404)
            else:
                data_que = Data.objects.filter(device=device).order_by("-date_created")[:1]
                j = 0
                for ht in data_que:
                    history = "["
                    data = ht.data_content.split(";")
                    history = history + "\"" + timezone.now().strftime("%H:%M:%S") + "\""

                    if (len(data) < len(dtpoint)):
                        for i in range(len(data), (len(dtpoint))):
                            data.append('0')
                    i = 0
                    for key in dtpoint:
                        history = history + "," + str(random.randint(0, 100)) #data[i]
                        i = i +1
                    history = history + "]"

                    if j > 0:
                        jsondata = jsondata + "," + history
                    else:
                        jsondata = jsondata + history
                    j = j + 1
                jsondata = jsondata + "]"
                return HttpResponse(jsondata, status=200)

#example
'''
http://127.0.0.1:8000/api/devm/v1/data/data/
[{
	"id": "8228dbdc-56ed-11ea-8a16-88d7f67ebb61",
	"tempure": 0,
	"humidity": 0
}]
'''
#
@csrf_exempt
def DeviceDataUpdate(request):
    if request.method == 'GET':
        return HttpResponse('not support get', status=401)

    if request.method == 'POST':
        devices = []
        body = request.body.decode('utf-8').replace(" ","")
        if not body:
            return HttpResponse('Token is not valid', status=401)
        try:
            data = json.loads(body)
            if not data:
                return HttpResponse('json data error', status=401)
            logger.debug("recv data:{}".format(data))
            queryset = Device.objects.filter(is_deleted=False)
            for dt in data:
                if not 'id' in dt:
                    return HttpResponse('json data error not have id', status=401)
                device_id = dt['id']
                logger.debug("device_id:{}".format(device_id))
                device = queryset.get(device_sn=device_id)
                if not device:
                    return HttpResponse('Not have device', status=401)
                devpoint = device_point_query(device)
                if devpoint is None:
                    return HttpResponse('Not have device', status=401)
                else:
                    content = ""
                    i = 0
                    for dp in devpoint:
                        if not dp.data_key in dt:
                            return HttpResponse('key setting error', status=401)
                        if(i>= 1):
                            content = content + ";" + str(dt[dp.data_key])
                        else:
                            content = str(dt[dp.data_key])
                        i = i + 1

                    Data.objects.create( data_content=content, device=device, date_created=timezone.now())
                    return HttpResponse('ok', status=201)


        except Device.DoesNotExist:
            return HttpResponse('Not have device', status=401)

        except:
            logger.exception("DeviceDataUpdate error")
            return HttpResponse('json data error', status=401)





#http://127.0.0.1:8888/api/devm/v1/data/reg/
'''
   [ {
        "device": "5487f877-fe77-11e7-8928-184f3260e267",
        "passwd": "123456"
    }]

'''

@csrf_exempt
def DeviceTokenApi(request):
    if request.method == 'GET':
        try:
            device_sn = request.query_params.get('device')
            passwd = request.query_params.get("passwd")

            if not device_sn or not passwd:
                return HttpResponse('Not have device id or passwd', status=401)

            queryset = Device.objects.filter(is_deleted=False)
            device = queryset.get(device_sn=device_sn)

        except Device.DoesNotExist:
            device = None

        if device is None:
            return HttpResponse('Not have device', status=401)

        if not passwd or (device.device_pwd != passwd):
            return HttpResponse("No password or password error", status=401)

        token = uuid.uuid4().hex
        cache.set(token, str(device.device_sn), 3600)
        data = {"token": token, "msg": "send device status"}
        return JsonResponse(data, status=201)

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        device_sn = ""
        passwd = ""

        try:
            if not body:
                return HttpResponse('Not have device id or passwd', status=401)
            else:
                data = json.loads(body)
                if not data:
                    return HttpResponse('Not recv json data', status=401)
                else:
                    if(len(data)>0):
                        data = data[0]          #只取一个
                    device_sn = data['device']
                    passwd = data['passwd']
                    print("device_sn:%s, passwd:%s" % (device_sn, passwd))
                    if not device_sn or not passwd:
                        return HttpResponse('Not have device id or passwd', status=401)
            queryset = Device.objects.filter(is_deleted=False)
            device = queryset.get(device_sn=device_sn)

        except Device.DoesNotExist:
            device = None
        except Exception as e:
            #print(e)
            device = None

        if device is None:
            return HttpResponse('Not have device', status=401)

        if not passwd or (device.device_pwd != passwd):
            return HttpResponse("No password or password error", status=401)

        token = uuid.uuid4().hex
        cache.set(token, str(device.device_sn), 3600)
        data = {"token": token, "msg": "send device status"}
        return JsonResponse(data, status=201)

