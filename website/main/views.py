from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from . import forms

from pytube import YouTube, Playlist 

# Create your views here.
def download(request):
    if request.method == "GET":
        if request.GET.get("download"):
            url = request.GET.get("download")
            item = YouTube(url)
            item.streams.get_audio_only().download()
        return HttpResponse('<script type="text/javascript">window.close()</script>')


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
            len(context["page_obj"].object_list) * self.get_page
            context["object_list"] = self.get_queryset().videos[(len(context["page_obj"].object_list) * (self.get_page -1)): (len(context["page_obj"].object_list) * self.get_page)]
            return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)