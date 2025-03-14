from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import MyUserManager

class User(AbstractBaseUser, PermissionsMixin):
    phone_number=models.CharField(max_length=11,unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    birth_date = models.DateField(blank=True, null=True)
    full_name=models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email','address', 'full_name']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin




class OtpCode(models.Model):
    phone_number=models.CharField(max_length=11, unique=True)
    otp_code=models.SmallIntegerField()
    created=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.otp_code} - {self.created}'


class Favorites(models.Model):

    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='faves')
    favorite_items=models.ForeignKey('self', on_delete=models.CASCADE)
    class Meta:
        verbose_name="Favorite"
        verbose_name_plural="Favorites"

    def __str__(self):
        return f'{self.user.full_name} likes {self.favorite_items}'






