from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)
    avatar = models.CharField(max_length=100, default='avatar9.png')  # Avatar 9 is default

    def __str__(self):
        return self.user.email


