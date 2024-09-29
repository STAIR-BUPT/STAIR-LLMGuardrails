from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import status

from .models import Token

import binascii
import os

# Create your views here.
def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()
    
@api_view(['POST'])
def generate_token(request):
    if request.user and request.user.is_authenticated:
        token = Token.objects.create(key=generate_key(), user=request.user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
