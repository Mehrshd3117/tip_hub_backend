from django.db import models
from accounts.models import User


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    desc = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    pup_date = models.DateField(auto_now_add=True)
    video_views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title

    def count_likes(self):
        return self.likes.count()


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name='subscribers')

    def __str__(self):
        return self.user.first_name
