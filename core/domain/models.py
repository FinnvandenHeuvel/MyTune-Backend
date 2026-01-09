from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    artist_id = models.CharField(max_length=100, blank=True, null=True)
    album = models.CharField(max_length=200, blank=True, null=True)
    album_id = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.rating}/5) by {self.user.username}"
