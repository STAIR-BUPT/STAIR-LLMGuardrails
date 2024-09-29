from django.urls import path
from .views import generate_token

urlpatterns = [
    path('api/token/', generate_token, name='generate_token'),
]
