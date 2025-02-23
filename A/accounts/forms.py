from .models import User, OtpCode
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
class UserCreationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='confirm password',widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'repeat your password'}))
    class Meta:
        model = User
        fields=['phone_number','email','address','birth_date','full_name']
        widgets= {
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'address':forms.Textarea(attrs={'class':'form-control'}),
            'birth_date':forms.DateInput(attrs={'class':'form-control','placeholder':'optional'}),
            'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'optional'})
        }

        labels={
            'phone_number':'your phone number',
            'birth_date':'your birth date',
            'full_name':'your full name'
        }


    def clean(self):
        cd=super().clean()
        p1=cd.get('password')
        p2=cd.get('password2')
        if p1 and p2 and p1!=p2:
            raise ValidationError('passwords do not match')
        return cd

    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user



class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text='you can change password <a href="../password/">by this link<a/>')
    class Meta:
        model=User
        fields=['phone_number','email','address','birth_date','full_name','password','last_login']



class UserRegisterForm(forms.Form):
    full_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    phone_number=forms.CharField(max_length=11,widget=forms.TextInput(attrs={'class':'form-control'}))
    address=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='confirm password',widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'repeat your password'}))

    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email has already registered!!')
        return email
    def clean_phone_number(self):
        phone_number=self.cleaned_data['phone_number']
        user=User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('this phone number has already registered!!')
        OtpCode.objects.filter(phone_number=phone_number).delete()
        return phone_number

class VerifyCodeForm(forms.Form):
    code=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))


class UserLoginForm(forms.Form):
    phone_number=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))














