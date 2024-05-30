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
        link = request.POST.get("link")
        you_tube = YouTube(link)
        
        # Get the thumbnail URL
        thumbnail_url = you_tube.thumbnail_url
        
        # Get all the video streams with their download URLs
        video_streams = you_tube.streams.filter(progressive=True, file_extension='mp4')
        download_links = []
        for stream in video_streams:
            download_links.append({
                "resolution": stream.resolution,
                "mime_type": stream.mime_type,
                "url": stream.url
            })
        
        # Pass the thumbnail URL and download URLs to the template
        return render(request, "partials/get-streams.html", {
            "stream_image": thumbnail_url,
            "download_links": download_links,
            "video_title": you_tube.title,
        })
