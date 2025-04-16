from django.urls import path
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
app_anme='api'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user_login/', views.UserLoginAPIView.as_view(), name='user_login'),
    path('add_cart/<int:pk>/', views.CartAPIView.as_view(), name='cart_add'),


]

register_router=routers.SimpleRouter()
register_router.register(r'user_register', views.UserRegisterAPIView,  basename='user-register')
urlpatterns += register_router.urls

product_router=routers.SimpleRouter()
product_router.register(r'products', views.ProductAPIView, basename='product-view')
urlpatterns+=product_router.urls

