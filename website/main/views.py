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
    search_query = forms.SearchQuary
    template_name = "index.html"
    
    def is_list(self):
        return self.request.GET.get("search").__contains__("list")
    
    def get_queryset(self):
        queryset = None
        if self.request.GET.get("search"):
            if self.is_list():
                queryset = Playlist(self.request.GET.get("search")).videos
            else:
                queryset = self.request.GET.get("search")
        return queryset
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["queryset"] = self.get_queryset()
        return context
    
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.request.GET.get("download"):
            url = self.request.GET.get("download")
            item = YouTube(url)
            item.streams.get_audio_only().download()
        return super().get(request, *args, **kwargs)

        