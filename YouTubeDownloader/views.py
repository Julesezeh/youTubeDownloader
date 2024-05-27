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

def get_streams(request):
    if request.method == "POST":
        print("I was called")
        link =  request.POST.get("link")
        you_tube = YouTube(link)
        # stream = you_tube.streams.get_highest_resolution()
        stream_image_url = you_tube.thumbnail_url

        return render(request, 'partials/get-streams.html',{'stream_image':stream_image_url})