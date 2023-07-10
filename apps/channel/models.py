from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Channel(models.Model):
    banner = models.URLField(verbose_name='Banner image URL', null=True, blank=True)
    picture = models.URLField(verbose_name='Avatar image URL', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channel_user')
    handle = models.CharField(blank=True, unique=True)
    contact_email = models.EmailField(verbose_name='Contact email', null=True, blank=True)
    subscription = models.ManyToManyField(User, through='ChannelSubscription', related_name='channel_subscription')

    def __str__(self):
        return self.user_profile.user.username


class ChannelSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    subscription_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.channel.handle