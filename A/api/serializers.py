from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import OtpCode, Favorites, User
from home.models import Product

# account serializer
def clean_phone_number(value):
    if len(value) !=11:
        raise serializers.ValidationError("this phone number is not valid")
    return value

class UserRegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True, required=True)
    class Meta:
        model=User
        fields=['phone_number','email','full_name','address', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only':True},
            'password2':{'write_only':True},
            'phone_number':{'validators':[clean_phone_number]},

        }

    def validate_email(self, value):
        if 'admin' in value:
            raise serializers.ValidationError("admin cant be inside your email!")
        return value

    def validate_full_name(self, value):
        if 'admin' in value:
            raise serializers.ValidationError("admin cant be inside your name!")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("the passwords dont match!")
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        user=User.objects.create_user(**validated_data)
        return user

# product serializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

# order serializer

class CartAddSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, max_value=9)

    class Meta:
        model = Product
        fields = ['quantity']











