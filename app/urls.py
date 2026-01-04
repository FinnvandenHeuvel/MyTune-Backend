from django.urls import path
from core.views import reviews
from core.views import register
from core.views import me, my_reviews, review_delete
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path("api/reviews/", reviews, name="reviews"),
    path("api/reviews/<int:pk>/", review_delete, name="review_delete"),
    path("api/me/", me, name="me"),
    path("api/my-reviews/", my_reviews, name="my_reviews"),

    path("api/register/", register, name="register"),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
