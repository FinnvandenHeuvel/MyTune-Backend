from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]  # allow anyone to POST

    def get_queryset(self):
        queryset = Review.objects.all().order_by('-created_at')
        artist_id = self.request.query_params.get('artist_id')
        if artist_id:
            queryset = queryset.filter(artist_id=artist_id)
        album_id = self.request.query_params.get('album_id')
        if album_id:
            queryset = queryset.filter(album_id=album_id)
        return queryset
