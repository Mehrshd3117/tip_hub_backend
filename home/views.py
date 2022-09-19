from django.shortcuts import render
from django.views import View
from django.db.models import Count, Q
from datetime import datetime, timedelta
# app model
from video.models import Video


class Home(View):
    def get(self, request, *args, **kwargs):
        last_month = datetime.today() - timedelta(days=30)
        latest_videos = Video.objects.all().order_by('-updated')[:6]
        most_viewed_videos = Video.objects.all().annotate(
            count=Count('views', filter=Q(videoview__created__gt=last_month))).order_by(
            '-count', '-created')[:6]
        context = {
            'videos': latest_videos,
            'video_views': most_viewed_videos
        }
        return render(request, 'home/index.html', context)
