# encoding: utf-8
import os
import time

import json

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView,DetailView
from .models import Picture
from .response import JSONResponse, response_mimetype
from .serialize import serialize
from iotserver import settings as setting
from uuslug import slugify
from .hands import AdminUserRequiredMixin


class PictureCreateView(CreateView):
    model = Picture
    fields = "__all__"


    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            myFile = request.FILES['file'] # 获取上传的文件，如果没有文件，则默认为None
            if not myFile:
                return HttpResponse(json.dumps({'success': 0, 'message': 'upload image failed'}, ensure_ascii=False),
                                    content_type="application/json")
            strs = myFile.name.split('.')
            suffix = strs[-1]
            file_name = slugify(strs[0])
            if not suffix or suffix not in setting.FILE_FORMATS:
                return HttpResponse(json.dumps({'success': 0, 'message': 'upload image failed'}, ensure_ascii=False),
                                    content_type="application/json")

            myFile.name = "%s.%s" %(file_name,suffix )
            pic = Picture.objects.create(file= myFile)
            pic.save()
            #print(pic.get_absolute_url())

            #return HttpResponse(json.dumps({'success': 1, 'message': 'upload image successed',
            #                                'url':''},
            #                               ensure_ascii=False), content_type="application/json")
            files = [serialize(pic)]
            data = {'files': files}
            response = JSONResponse(data, mimetype=response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class PictureDeleteView(AdminUserRequiredMixin, DetailView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(ListView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureDetailView(AdminUserRequiredMixin, DetailView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_object()() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
