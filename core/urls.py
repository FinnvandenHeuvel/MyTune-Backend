from django.urls import path, include

urlpatterns = [
    path('', include('app.urls')),  # use your app folder name here
]
