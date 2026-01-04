from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Review
from core.serializers import ReviewSerializer, MeSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(MeSerializer(request.user).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_reviews(request):
    queryset = Review.objects.filter(user=request.user).order_by("-created_at")
    serializer = ReviewSerializer(queryset, many=True)
    return Response(serializer.data)
