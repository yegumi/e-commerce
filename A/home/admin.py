from django.contrib import admin
from . models import Category, Product , Comment

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ['category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sub_category', 'is_sub')  # You can customize this as per your need
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'body')
