# app/views.py
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Hello! Your Django route is working.")
