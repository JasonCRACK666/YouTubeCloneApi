from django.db import models

from apps.channel.models import Channel
from apps.user_profile.models import Profile

class Video(models.Model):
    title = models.CharField(max_length=45)
    video_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)
    views = models.ManyToManyField(Profile, through='VideoView')

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

class VideoView(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    count = models.PositiveBigIntegerField(default=1)
    last_view_date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self) -> str:
        return self.video.title