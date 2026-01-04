from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import Review
from ..serializers import ReviewSerializer, MeSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def reviews(request):
    # GET: list reviews (optionally filtered)
    if request.method == "GET":
        artist_id = request.GET.get("artist_id")
        album_id = request.GET.get("album_id")

        queryset = Review.objects.all().order_by("-created_at")

        if artist_id:
            queryset = queryset.filter(artist_id=artist_id)

        if album_id:
            queryset = queryset.filter(album_id=album_id)

        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST: create review (must be authenticated)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # user comes from JWT
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def review_delete(request, pk):
    # Only "admin" users can delete (staff or superuser)
    if not (request.user.is_staff or request.user.is_superuser):
        return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(MeSerializer(request.user).data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_reviews(request):
    queryset = Review.objects.filter(user=request.user).order_by("-created_at")
    serializer = ReviewSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
