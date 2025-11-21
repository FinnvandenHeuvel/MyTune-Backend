from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from core.models import Review
from ..serializers import ReviewSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def reviews(request):
    if request.method == "GET":
        artist_id = request.GET.get("artist_id")
        album_id = request.GET.get("album_id")

        queryset = Review.objects.all().order_by("-created_at")

        if artist_id:
            queryset = queryset.filter(artist_id=artist_id)

        if album_id:
            queryset = queryset.filter(album_id=album_id)

        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
