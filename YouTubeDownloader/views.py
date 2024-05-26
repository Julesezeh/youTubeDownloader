from django.shortcuts import render
from pytube import YouTube

def index(request):
    if request.method == "POST":
        link =  request.POST.get("link")
        you_tube = YouTube(link)
        stream = you_tube.streams.get_highest_resolution()
        stream.download()
        return render(request,"index.html")
    return render(request,"index.html")