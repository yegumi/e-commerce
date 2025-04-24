from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from accounts.models import User, OtpCode
from home.models import Product
from orders.cart import Cart
from orders.models import OrderItem
from .serializers import UserRegisterSerializer, ProductSerializer, CartAddSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from utils import send_otp_code
from datetime import datetime, timedelta
import random
import pytz

# accounts views
class UserRegisterAPIView(viewsets.ViewSet):
    serializer_class=UserRegisterSerializer
    def create(self, request):
        if request.user and request.user.is_authenticated:
            return Response({"detail": "You are already logged in."}, status=status.HTTP_400_BAD_REQUEST)
        ser_data=UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            validated_data_copy = ser_data.validated_data.copy()
            validated_data_copy.pop('password', None)
            validated_data_copy.pop('password2', None)
            return Response(validated_data_copy, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        phone_number=request.data['phone_number']
        password=request.data['password']
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            # If authentication is successful, create JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'refresh': str(refresh),
                'access': access_token
            }, status=status.HTTP_200_OK)

        return Response({
            'detail': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    pass
#   loging out will be decided in future idk if i should handle it in front-end by removing client data  from client side or not

# home views

class ProductAPIView(viewsets.ViewSet):
    serializer_class=ProductSerializer
    querysets = Product.objects.all()
    def list(self, request):
        ser_data=ProductSerializer(instance=self.querysets, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)
    def retrieve(self, request,pk):
        product=get_object_or_404(self.querysets, pk=pk)
        ser_data=ProductSerializer(instance=product)
        return Response(ser_data.data, status=status.HTTP_200_OK)

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart(request)
        items = list(cart)
        total_price = sum(item["total_price"] for item in items)

        response_data = {
            "items": [
                {
                    "product_id": item["product"].id,
                    "product_name": item["product"].name,
                    "price": str(item["product"].price),
                    "quantity": item["quantity"],
                    "total": str(item["total_price"]),
                }
                for item in items
            ],
            "total_price": str(total_price)
        }

        return Response(response_data, status=status.HTTP_200_OK)


    def post(self, request, pk):
        serializer_class=CartAddSerializer
        """ the cart we add here is the one we clicked on, in the ProductAPIView"""
        product=get_object_or_404(Product, pk=pk)
        ser_data=CartAddSerializer(data=request.data)
        cart=Cart(request)
        if ser_data.is_valid():
            cart.add(product, ser_data.validated_data['quantity'])
            cart.save()
            return Response({'detail': 'Product added to cart'}, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product=get_object_or_404(Product, pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "product not found."}, status=status.HTTP_404_NOT_FOUND)
        cart = Cart(request)
        cart.remove(product)
        return Response({'message':'deleted'}, status=status.HTTP_200_OK)








