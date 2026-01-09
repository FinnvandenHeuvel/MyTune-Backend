from django.urls import path
from django.http import JsonResponse
from core.interface.api.views.reviews import reviews, review_delete
from core.interface.api.views.profile import me, my_reviews
from core.interface.api.views.auth import register

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def healthz(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("healthz/", healthz),
    path("reviews/", reviews, name="reviews"),
    path("reviews/<int:pk>/", review_delete, name="review_delete"),
    path("me/", me, name="me"),
    path("my-reviews/", my_reviews, name="my_reviews"),
    path("register/", register, name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
