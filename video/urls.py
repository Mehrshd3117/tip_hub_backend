from django.urls import path
from . import views

app_name = 'videos'
urlpatterns = [
    path('video_list', views.video_list, name='video_list'),
    path('video_detail/<slug:slug>', views.video_detail, name='video_detail'),
    path('video_delete/<int:pk>', views.video_delete, name='video_delete'),
    path('video_edit/<int:pk>', views.VideoEditView.as_view(), name='video_edit'),
    path('category/<slug:slug>', views.category_detail, name='category_detail'),
    path('subscribe/<int:pk>', views.subscribe_add, name='sub_add'),
    path('like/<slug:slug>/<int:pk>', views.like, name='like'),
    path('search/', views.search_list, name='search'),
]
