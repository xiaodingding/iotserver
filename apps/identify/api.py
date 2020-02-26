# ~*~ coding: utf-8 ~*~
# import uuid
from PIL import Image
from django.core.cache import cache
from django.shortcuts import get_object_or_404


from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import BulkModelViewSet

from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse

from common.mixins import CustomFilterMixin
from common.utils import get_logger
from .models import  Identify
from .hands import IsSuperUser
from .utils import *



from .serializers import *
import json as sp_json

logger = get_logger(__name__)



class IdentifyViewSet(CustomFilterMixin, BulkModelViewSet):
    queryset = Identify.objects.all()
    serializer_class = IdentifySerializer
    permission_classes = (IsSuperUser, IsAuthenticated)


@method_decorator(csrf_exempt, name='dispatch')
class IdentifyToken(View):
    permission_classes = (AllowAny,)
    def get(self, request):
        return HttpResponse("not support get method", status=406)

    def post(self, request):
        if not request.user.is_authenticated:
            if len(request.POST) < 2:
                request_body = request.body.decode()
                logger.debug("request_body{}".format( request_body) )
                receive_data = sp_json.loads(request_body)
                username = receive_data.get('username', '')
                password = receive_data.get('password', '')
                email = receive_data.get('email', '')
                softid = receive_data.get('softid', '')
            else:
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                email = request.POST.get('email', '')
                softid = request.POST.get('softid', '')
            log = "username:{}, password:{}, email:{}, softid:{}".format(username, password, email, softid)
            logger.debug(log)

            user, msg = check_identify_valid(
                username=username, email=email,
                password=password, softid=softid)
            logger.debug("request not auth user:{}".format(user))
        else:
            user = request.user
            logger.debug("request have auth user:{}".format(user))
            msg = None
        if user:
            token = generate_identify_token(request, user.username)
            json = {'token': token}
            return JsonResponse(json, status=201)
        else:
            json = {'error': msg}
            return JsonResponse(json, status=406)

@method_decorator(csrf_exempt, name='dispatch')
class ImageIdentifyAPI(View):
    # import .helper as helppp
    permission_classes = (AllowAny,)
    def post(self, request):
        image = request.FILES.get('images')
        # request_body  = getattr(request,'_body',request.body)

        if not image:
            json = {'error': "image not find"}
            return JsonResponse(json, status=406)

        if len(request.POST) < 1:
            request_body = request.body.decode()
            logger.debug("request_body{}".format( request_body) )
            receive_data = sp_json.loads(request_body)
            token = receive_data.get('token')
            username = receive_data.get('username', '')
        else:
            token = request.POST.get('token', '')
            username = request.POST.get('username', '')
        if not token:
            json = {'error': "not find token"}
            return JsonResponse(json, status=406)

        logger.debug("request_body token:{}".format(token ))

        val_token = validate_token(request, username)
        if(val_token != token):
            json = {'error': "token error"}
            return JsonResponse(json, status=406)

        # img_rect = imageRectFromImage(image.file)
        # img_rect = imageRectFromImage(image.file)
        image = Image.open(image)
        # print(type(image))
        # img_rect = None
        img_rect = imageRectFromImage(image)
        if img_rect:
            json = {'result': img_rect}
            return JsonResponse(json, status=201)
        else:
            json = {'error': "imgae recognize fail"}
            return JsonResponse(json, status=406)


