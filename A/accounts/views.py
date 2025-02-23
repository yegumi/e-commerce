from django.shortcuts import render, redirect
from django.views import View
from . forms import UserRegisterForm, VerifyCodeForm, UserLoginForm
from . models import User, OtpCode
from django.contrib import messages
from django.contrib.auth import logout, authenticate , login
import random
from utils import send_otp_code
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime,timedelta
import pytz


class UserRegisterView(View):
    form_class=UserRegisterForm
    teplate_name='accounts/register.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        return render(request,self.teplate_name,{'form':self.form_class})
    def post(self, request):
        form=self.form_class(request.POST)
        if form.is_valid():
            random_code=random.randint(1000,9999)
            send_otp_code(form.cleaned_data['phone_number'],random_code)

            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], otp_code=random_code)
            request.session['user_registration_info']={
                'phone_number':form.cleaned_data['phone_number'],
                'email':form.cleaned_data['email'],
                'full_name':form.cleaned_data['full_name'],
                'address':form.cleaned_data['address'],
                'password':form.cleaned_data['password'],
            }
            messages.success(request,'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        else:
            return render(request,self.teplate_name,{'form':form})

class UserRegisterVerifyCode(View):
    form_class=VerifyCodeForm
    def get(self, request):
        form=self.form_class()
        return render(request, 'accounts/verify.html',{'form':form})


    def post(self, request):
        user_session = request.session['user_registration_info']
        form=self.form_class(request.POST)
        code_instance=OtpCode.objects.get(phone_number=user_session['phone_number'])
        if form.is_valid():
            cd=form.cleaned_data
            if cd['code']== code_instance.otp_code:
                now=datetime.now(tz=pytz.UTC)
                if code_instance.created + timedelta(minutes=2)< now:
                    messages.error(request, 'your code is expired!', 'danger')
                    return redirect('accounts:register')
                User.objects.create_user(phone_number=user_session['phone_number'], email=user_session['email'], address=user_session['address'], full_name=user_session['full_name'],
                                         password=user_session['password'])
                messages.success(request,'you registered successfully','success')
                code_instance.delete()
            else:
                messages.error(request,'your code is wrong!','warning')
                return redirect ('accounts:verify_code')
        return redirect('home:home')

class UserloginView(View):
    form_class=UserLoginForm
    template_name='accounts/login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch( request, *args, **kwargs)
    def setup(self, request, *args, **kwargs):
        self.next=request.GET.get('next',None)
        return super().setup(request, *args,**kwargs)
    def get(self, request):
        form=self.form_class
        return render(request,self.template_name, {'form':form} )
    def post(self, request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,f' welcome back {user.full_name}', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request,f' the login entries are not diagnosed ', 'danger')
        return redirect('accounts:login')

class UserLogoutView(LoginRequiredMixin,View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'you logged out')
        return redirect('home:home')






