from pytube import YouTube, Playlist


url_playlist = "https://www.youtube.com/watch?v=pTCp0kJYF30&list=PLWeQEniCrtoEy47FUl0WmL4hn2IqjF_x3"
url = "https://www.youtube.com/watch?v=KyhrqbfEgfA"
yt = Playlist(url_playlist).videos

print(yt)
init_stream = YouTube(yt)


    

#print(init_stream.streams.filter(only_audio=True))
# init_stream.streams.get_audio_only().download()