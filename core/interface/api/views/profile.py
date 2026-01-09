from django.views.decorators.http import require_GET
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.application.services.profile_service import get_my_reviews
from core.interface.api.serializers import MeSerializer, ReviewSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@require_GET
def me(request):
    return Response(MeSerializer(request.user).data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@require_GET
def my_reviews(request):
    queryset = get_my_reviews(user=request.user)
    return Response(
        ReviewSerializer(queryset, many=True).data, status=status.HTTP_200_OK
    )
