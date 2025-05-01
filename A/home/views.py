from django.shortcuts import render, redirect , get_object_or_404
from django.views import View
from .forms import CommentForm, ReplyForm
from .models import Product, Category , Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from .tasks import all_bucket_objects_tasks
from orders.forms import CartAddForm
from . import tasks
from django.contrib import messages
from utils import IsUserAdminMixin

class HomeView(View):
    def get(self, request):
       return render(request, 'home/index.html')

class AboutMeView (View):
    def get(self, request):
        return render(request, 'home/aboutme.html')

class FAQ(View):
    def get(self, request):
        return render(request, 'home/faq.html')




class ProductView(View):
    def get(self, request):
        products=Product.objects.filter(available=True)
        return render(request,'home/product.html', {'products': products})
    def post(self, request):
        pass

class ProductDetailView(LoginRequiredMixin,View):
    def get(self, request , product_id):
        product=get_object_or_404(Product,id=product_id )
        form=CartAddForm()
        reply = CommentForm()
        return render (request,'home/detail.html',{'product': product,'form':form,'reply':reply } )

    def post(self, request, product_id, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        reply_form = CommentForm(request.POST)

        if reply_form.is_valid():
            cd = reply_form.cleaned_data
            parent_comment = Comment.objects.get(id=comment_id)

            Comment.objects.create(
                user=request.user,
                body=cd['body'],
                product=get_object_or_404(Product, id=product_id),
                reply=parent_comment,
                is_reply=True
            )

        return redirect('home:detail', product_id=product_id)


class CategoryView(View):
    def get(self, request):
        categories=Category.objects.filter(is_sub=False)
        return render (request,'home/category.html',{'categories':categories})
    def post(self, request):
        pass

class CategoryDetailView(View):
    def get(self, request, slug_id):
        category=get_object_or_404(Category, slug=slug_id)
        products = Product.objects.filter(category=category)
        return render(request, 'home/category_detail.html', {'products': products})


class AddCommentView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = CommentForm()
        return render(request, 'home/add_comment.html', {'product': product, 'form': form, })

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            Comment.objects.create(user=request.user,product=product,body=cd['body'])
            return redirect('home:detail', product_id=product.id)
            # if form is invalid, re-render with errors
        return render(request, 'home/add_comment.html', {'product': product, 'form': form})







class BucketHomeView(IsUserAdminMixin, View):
    def get(self, request):
        objects=tasks.all_bucket_objects_tasks()
        # print('*'*100)
        # print(objects)
        # if we had celery we should call it with delay but we didn't write its asyn cause we dont know how to code in js
        return render (request, 'home/bucket.html',{'objects':objects})



class BucketDeleteView(IsUserAdminMixin,View):
    def get(self, request , key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'your object will be deleted soon' , 'info')
        return redirect ("home:bucket")


class BucketDownloadView(IsUserAdminMixin,View):
    def get(self, request, key ):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your object will be downloaded soon', 'info')
        return redirect("home:bucket")

class BucketUploadView(IsUserAdminMixin,View):
    def get(self, request, key):
        tasks.upload_object_task(key)
        messages.success(request, 'your object will be uploaded soon ', 'info')
        return redirect("home:bucket")