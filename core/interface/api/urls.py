from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core.interface.api.views.auth import register
from core.interface.api.views.profile import me, my_reviews
from core.interface.api.views.reviews import (
    review_delete,
    reviews_create,
    reviews_list,
)

urlpatterns = [
    # Reviews
    path("reviews/", reviews_list, name="reviews-list"),
    path("reviews/new/", reviews_create, name="reviews-create"),
    path("reviews/<int:pk>/", review_delete, name="review-delete"),
    # Profile
    path("me/", me, name="me"),
    path("my-reviews/", my_reviews, name="my-reviews"),
    # Auth
    path("register/", register, name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
