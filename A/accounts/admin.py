from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm , UserChangeForm
from django.contrib.auth.models import Group
from .models import User, OtpCode, Favorites

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display=['full_name','email','birth_date','is_admin']
    list_filter = ['is_admin']
    fieldsets = (
        (None,{'fields':('full_name','email','phone_number','birth_date','address','password')}),
               ('permissions',{'fields':('is_active','is_admin','is_superuser','groups', 'user_permissions','last_login')}),

                 )
    add_fieldsets = (
        (None, {
            'fields': ('full_name', 'email', 'phone_number', 'birth_date', 'address', 'password', 'password2')
        }),
    )

    search_fields = ('email','full_name')
    ordering=['full_name']
    filter_horizontal = ['groups','user_permissions']
    readonly_fields = ['last_login']

    def get_form(self, request, obj=None, **kwargs):
        form=super().get_form(request, obj, **kwargs)
        is_superuser=request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled =True
        return form



admin.site.register(User, UserAdmin)

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display=['phone_number','otp_code','created']

@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display=['user','favorite_items']






