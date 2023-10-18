from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from . import forms

from pytube import YouTube, Playlist
import os

# Create your views here.
def download(request):
    if request.method == "GET":
        if request.GET.get("download"):
            url = request.GET.get("download")
            item = YouTube(url)
            file_path = item.streams.get_audio_only().download()
            print("____________________________________")
            print(item.streams.get_audio_only().audio_codec)
            with open(file_path, 'rb') as fh:
                HttpResponse('<script type="text/javascript">window.close()</script>')
                response = HttpResponse(fh.read(), content_type="application/file")
                response['Content-Disposition'] = 'inline; filename={}'.format(file_path)
                
                item.streams.get_audio_only().on_complete(file_path)
                
                os.remove(file_path)
                return response
            
        return


class ListView(generic.ListView):
    template_name = "index.html"
    paginate_by = 25
    queryset = None
    
    @property
    def get_search_query(self):
        return self.request.GET.get("query")
    
    @property
    def get_page(self):
        if self.request.GET.get("page"):
            return int(self.request.GET.get("page"))
        return 1
    
    @property
    def is_list(self):
        return 'list' in self.get_search_query # self.request.GET.get("search").__contains__("list")
    
    def get_queryset(self):
        if self.get_search_query:
            if self.is_list:
                self.queryset = Playlist(self.get_search_query)
            else:
                self.queryset = self.get_search_query
        return self.queryset
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        if self.get_queryset():
            context = super().get_context_data(**kwargs)
            context["object_list"] = self.get_queryset().videos[(len(context["page_obj"].object_list) * (self.get_page -1)): (len(context["page_obj"].object_list) * self.get_page)]
            return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)