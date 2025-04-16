from django.urls import path
from . import views


app_name='accounts'
urlpatterns=[
    path('register/',views.UserRegisterView.as_view(),name='register'),
    path('verify',views.UserRegisterVerifyCode.as_view(), name='verify_code'),
    path('login/',views.UserloginView.as_view(), name='login'),
    path('logout/',views.UserLogoutView.as_view(), name='logout')
]

