from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from accounts.models import User
from .models import Video, Subscriber, Like, Category
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView
from django.db.models import Q


def video_list(request):
    video = Video.objects.all()
    # Pagination
    page = request.GET.get('page')
    paginator = Paginator(video, 6)
    objects_list = paginator.get_page(page)

    context = {
        'videos': objects_list
    }
    return render(request, 'video/video_list.html', context)


def video_detail(request, slug):
    video = get_object_or_404(Video.objects.all(), slug=slug)

    fav = False

    if video.favourites.filter(id=request.user.id).exists():
        fav = True

    ip_address = request.user.ip_address
    if ip_address not in video.views.all():
        video.views.add(ip_address)

    account = video.admin
    is_self = True
    user = request.user

    if user.is_authenticated and user != account:
        is_self = False

    context = {
        'video': video,
        'is_self': is_self,
        'fav': fav
    }
    if request.user.is_authenticated:
        if request.user.like.filter(video__slug=slug, user_id=request.user.id).exists():
            context['is_liked'] = True
        else:
            context['is_liked'] = False
    else:
        return redirect('accounts:login')
    return render(request, 'video/video_detail.html', context)


def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
    return redirect('videos:video_list')


def like(request, slug, pk):
    try:
        like = Like.objects.get(video__slug=slug, user_id=request.user.id)
        like.delete()
        return JsonResponse({"response": "unliked"})
    except:
        Like.objects.create(video_id=pk, user_id=request.user.id)
        return JsonResponse({"response": "liked"})


def subscribe_add(request, pk):
    all_subscriber = Subscriber.objects.get_or_create(user=User.objects.get(id=pk))[0]
    user_subscriber = User.objects.get(pk=request.user.id)

    if user_subscriber in all_subscriber.subscribers.all():
        all_subscriber.subscribers.remove()
        subscribed = True
        return JsonResponse(subscribed, safe=False)
    else:
        all_subscriber.subscribers.add()
        subscribed = False
        return JsonResponse(subscribed, safe=False)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    videos = category.video_category.all()

    # pagination
    page_number = request.GET.get('page')
    paginator = Paginator(videos, 3)
    objects_list = paginator.get_page(page_number)

    context = {
        "videos": objects_list,
        "category": category
    }
    return render(request, 'video/category_detail.html', context)


def search_list(request):
    q = request.GET.get('q')
    video = Video.objects.filter(
        Q(title__icontains=q) | Q(description__icontains=q))
    paginator = Paginator(video, 2)
    page = request.GET.get('page')
    objects_list = paginator.get_page(page)
    return render(request, 'video/search_list.html', context={'videos': objects_list})


class VideoEditView(UpdateView):
    model = Video
    template_name = 'video/video_edit.html'
    fields = ['title', 'video', 'description']

    def get_absolute_url(self):
        return reverse('videos:video_detail')
