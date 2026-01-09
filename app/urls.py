from django.urls import path, include
from django.http import JsonResponse

def healthz(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("healthz/", healthz),
    path("api/", include("core.interface.api.urls")),
]
