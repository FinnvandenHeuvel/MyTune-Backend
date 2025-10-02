from django.db import models

class Review(models.Model):
    name = models.CharField(max_length=100)   # reviewer name
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1–5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.rating}/5) by {self.name}"
