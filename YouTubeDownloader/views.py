from django.shortcuts import render
from pytube import YouTube
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, Http404

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
                "url": stream.url,
                "itag": stream.itag,  # Use itag to identify the stream
                "video_id": you_tube.video_id  # Use video_id to uniquely identify the video
            })

        print(download_links)
        
        # Pass the thumbnail URL and download URLs to the template
        return render(request, "partials/get-streams.html", {
            "stream_image": thumbnail_url,
            "download_links": download_links,
            "video_title": you_tube.title,
        })

@csrf_exempt
def get_download_url(request):
    print('get download url called')
    if request.method == "POST":
        itag = request.POST.get("itag")
        video_id = request.POST.get("video_id")
        try:
            # Reconstruct the YouTube URL from the video ID
            link = f"https://www.youtube.com/watch?v={video_id}"
            you_tube = YouTube(link)
            stream = you_tube.streams.get_by_itag(itag)
            download_url = stream.url
            return JsonResponse({"download_url": download_url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponseNotFound("The requested resource was not found.")