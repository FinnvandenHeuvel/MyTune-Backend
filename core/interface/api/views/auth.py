from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.interface.api.serializers import UserRegisterSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
@require_POST
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
    )
