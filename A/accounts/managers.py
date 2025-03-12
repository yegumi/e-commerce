from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number,email,address,password,full_name):
        if not phone_number:
            raise ValueError('user must have phone number')
        if not email:
            raise ValueError('user must have an email')
        if not address:
            raise ValueError('user must have address')

        user=self.model(phone_number=phone_number,email=self.normalize_email(email),address=address, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, phone_number,email,address,password,full_name):
        user=self.create_user( phone_number,email,address,password,full_name)
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user