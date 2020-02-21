# ~*~ coding: utf-8 ~*~
# import uuid

from django.core.cache import cache
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import BulkModelViewSet

from common.mixins import CustomFilterMixin
from common.utils import get_logger
from nav.models import Site, Category, SiteInfo
from .hands import IsSuperUser

from .serializers import *

logger = get_logger(__name__)


class CategoryViewSet(CustomFilterMixin, BulkModelViewSet):
    # queryset = User.objects.all().exclude(role="App").order_by("date_joined")
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsSuperUser, IsAuthenticated)
    # filter_fields = ('username', 'email', 'name', 'id')

    # def get_queryset(self):
    #     if self.object.pk:
    #         queryset = Category.objects.filter(id=self.object.pk).all()
    #     else:
    #         queryset = Category.objects.all()
    #     return queryset


class SiteViewSet(CustomFilterMixin, BulkModelViewSet):
    queryset = Site.objects.all()
    permission_classes = (IsSuperUser, IsAuthenticated)
    serializer_class = SiteSerializer

class SiteInfoViewSet(CustomFilterMixin, BulkModelViewSet):
    queryset = SiteInfo.objects.all()
    permission_classes = (IsSuperUser, IsAuthenticated)
    serializer_class = SiteInfoSerializer

class CategorySiteViewSet(APIView):
    model = Site
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        sites = Site.objects.filter(smallcategory=pk)
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data)

class CategoryDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(request.user.to_json())

    def post(self, request):
        return Response(request.user.to_json())


class SiteDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(request.user.to_json())

    def post(self, request):
        return Response(request.user.to_json())



class CategoryListAsTreeApi(generics.ListAPIView):
    """
    获取节点列表树
    [
      {
        "id": "",
        "name": "",
        "pId": "",
        "meta": ""
      }
    ]
    """
    model = Category
    permission_classes = (IsAuthenticated,)
    serializer_class = CategoryTreeSerializer

    def get_queryset(self):
        pk = self.request.query_params.get('pk')
        if pk:
            queryset = Category.objects.filter(id=pk)
        else:
            queryset = Category.objects.filter(parent_id=None).all()
        return queryset



# class NodeViewSet(OrgModelViewSet):
#     model = Node
#     filter_fields = ('value', 'key', 'id')
#     search_fields = ('value', )
#     permission_classes = (IsOrgAdmin,)
#     serializer_class = serializers.NodeSerializer

#     # 仅支持根节点指直接创建，子节点下的节点需要通过children接口创建
#     def perform_create(self, serializer):
#         child_key = Node.org_root().get_next_child_key()
#         serializer.validated_data["key"] = child_key
#         serializer.save()

#     def perform_update(self, serializer):
#         node = self.get_object()
#         if node.is_org_root() and node.value != serializer.validated_data['value']:
#             msg = _("You can't update the root node name")
#             raise ValidationError({"error": msg})
#         return super().perform_update(serializer)

#     def destroy(self, request, *args, **kwargs):
#         node = self.get_object()
#         if node.has_children_or_contains_assets():
#             msg = _("Deletion failed and the node contains children or assets")
#             return Response(data={'msg': msg}, status=status.HTTP_403_FORBIDDEN)
#         return super().destroy(request, *args, **kwargs)
