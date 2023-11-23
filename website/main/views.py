from typing import Any
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from . import forms

from pytube import YouTube, Playlist
import os

# Create your views here.
def download(request, watch_id):
    if request.method == "GET":
        if watch_id:
            url = YouTube(f"https://youtube.com/watch?v={watch_id}")
            file_path = url.streams.get_audio_only().download()
            print("____________________________________")
            print(url.streams.get_audio_only().audio_codec)
            with open(file_path, 'rb') as fh:
                HttpResponse('<script type="text/javascript">window.close()</script>')
                response = HttpResponse(fh.read(), content_type="audio/mpeg")
                response['Content-Disposition'] = 'attachment; filename={}.mp3'.format(url.author + " - " + url.title)
                
                url.streams.get_audio_only().on_complete(file_path)
                
                os.remove(file_path)
                return response
            
        return


class ListView(generic.ListView):
    template_name = "index.html"
    paginate_by = 2
    queryset = None
    
    @property
    def get_search_query(self):
        if self.request.POST.get("query") is None and self.request.session:
            return self.request.session['query']
        return self.request.POST.get("query")
    
    @property
    def get_page(self):
        if self.request.GET.get("page"):
            return int(self.request.GET.get("page"))
        return 1
    
    @property
    def is_list(self):
        """
        :return: True if 'list' in url params
        """
        if self.get_search_query:
            return 'list' in self.get_search_query # self.request.GET.get("search").__contains__("list")
    
    def get_queryset(self):
        if self.is_list:
            self.queryset = self.get_cached_playlist(self.get_search_query)
            print(len(self.queryset))
        elif self.is_list is not None:
            self.queryset = [YouTube(self.get_search_query)]
        return self.queryset
    
    def get_cached_playlist(self, query):
        cached_playlist = cache.get(query)
        if cached_playlist is None:
            # If not found in the cache, create a new Playlist object
            new_playlist = list(Playlist(query).videos)
            # Store the new playlist in the cache for future use
            cache.set(query, new_playlist)
            return new_playlist
        return cached_playlist
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        if self.queryset:
            context = super().get_context_data(**kwargs)
            return context
        return
        # if self.paginate_by:
        #     # start_index = len(context["page_obj"].object_list) * (self.get_page -1)
        #     # end_index = len(context["page_obj"].object_list) * self.get_page
        #     context["object_list"] = context["object_list"] = context['paginator'].get_page(self.get_page).object_list
        #     return context

    def post(self, request, *args, **kwargs):
        query_param = self.request.POST.get('query', '')
        self.request.session['query'] = query_param
        return self.get(request, *args, **kwargs)