from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.application.services.reviews_service import (
    create_new_review,
    delete_review_as_admin,
    get_reviews,
)
from core.interface.api.serializers import ReviewSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def reviews(request):
    if request.method == "GET":
        artist_id = request.GET.get("artist_id")
        album_id = request.GET.get("album_id")
        queryset = get_reviews(artist_id=artist_id, album_id=album_id)
        return Response(
            ReviewSerializer(queryset, many=True).data, status=status.HTTP_200_OK
        )

    serializer = ReviewSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    review = create_new_review(
        user=request.user, validated_data=serializer.validated_data
    )
    return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def review_delete(request, pk):
    _, err = delete_review_as_admin(user=request.user, pk=pk)
    if err == "Not allowed":
        return Response({"detail": err}, status=status.HTTP_403_FORBIDDEN)
    if err == "Not found":
        return Response({"detail": err}, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)
