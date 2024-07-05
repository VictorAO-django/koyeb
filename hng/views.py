from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import user_logged_in
from django.utils import timezone

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from .models import *
from .serializers import *
from .helpers import *


class Stage1_TaskView(APIView):
    @swagger_auto_schema(
        operation_summary="Returns client_ip, location(city), greetings",
        operation_description="Provide the product_id in the query param. \nEnsure a valid token is in the request headers - key = Authorization",
        operation_id="stage1",
        manual_parameters=[
            openapi.Parameter('visitor_name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
        responses={
            200: "Successful",
        }
    )
    def get(self, request, *args, **kwargs):
        visitor_name= request.query_params.get('visitor_name', 'Unknown user')
        ip = get_client_ip(request)
        location, temperature = get_location_temperature(ip)
        
        response = {
            "client_ip": ip, #Ip address of the requester
            "location": location, #city of the requester
            "greeting": f"Hello {visitor_name}, the temperature is {temperature} degrees in New York"
        }
        
        return Response(response, status=status.HTTP_200_OK)
# Create your views here.
