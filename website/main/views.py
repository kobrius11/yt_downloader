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
    paginate_by = 50
    queryset = None
    
    @property
    def get_search_query(self):
        return self.request.GET.get("search")
    
    def get_page(self):
        if self.request.GET.get('page'):
            print(self.request.GET.get('page'))
            return int(self.request.GET.get('page'))
        print(self.request.GET.get('page'))
        return 1
            
    def is_list(self):
        return 'list' in self.get_search_query # self.request.GET.get("search").__contains__("list")
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def get_queryset(self):
        if self.get_search_query():
            if self.is_list():
                self.queryset = Playlist(self.get_search_query)
            else:
                self.queryset = self.get_search_query
        return self.queryset
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(object_list = self.get_queryset(), **kwargs)
        context["object_list"] = context["paginator"].page(self.get_page()).object_list
        context["url"] = self.request.get_full_path()
        return context

        