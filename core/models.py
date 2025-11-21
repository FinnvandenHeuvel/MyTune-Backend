from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)  # Artist name
    artist_id = models.CharField(max_length=100, blank=True, null=True)  # Spotify ID
    album = models.CharField(max_length=200, blank=True, null=True)  # Album name
    album_id = models.CharField(max_length=100, blank=True, null=True)  # Album ID
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1–5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.rating}/5) by {self.user.username}"
