from django.db import models
from django.conf import settings
from django.utils.text import slugify


User = settings.AUTH_USER_MODEL


class Category(models.Model):
    sub_category=models.ForeignKey('self', on_delete=models.CASCADE,related_name='category',null=True, blank=True)

    is_sub=models.BooleanField(default=False)
    name=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['name']
        verbose_name='category'
        verbose_name_plural='categories'

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image=models.ImageField(upload_to='products/images/',null=True,)
    video = models.FileField(upload_to='product_videos/', null=True, blank=True)
    description= models.TextField()
    price=models.FloatField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    available=models.BooleanField(default=True)

    def __str__(self):
        return self.name





class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments')
    body=models.TextField(max_length=400)
    reply=models.ForeignKey('self', on_delete=models.CASCADE,related_name='rcomments', blank=True, null=True)
    is_reply=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)




