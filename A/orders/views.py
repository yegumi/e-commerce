from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm, CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionDenied
from .models import Order, OrderItem,Coupon
import datetime
from django.contrib import messages


class CartView(View):
	def get(self, request):
		cart = Cart(request)
		return render(request, 'orders/cart.html', {'cart':cart})


class CartAddView(View):
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.has_perm('orders.add_order'):
    #         raise PermissionDenied
    #
    #     return super().dispatch(request, *args, **kwargs)
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')

class CartRemoveView(View):
    def get(self,request, product_id):
        cart=Cart(request)
        product=get_object_or_404(Product,id=product_id)
        cart.remove(product)
        return redirect("orders:cart")

class OrderDetailView(LoginRequiredMixin,View):
    coupon_form=CouponApplyForm
    def get(self, request, order_id):
        order=get_object_or_404(Order,id=order_id)
        return render(request, "orders/order.html", {"order":order, "form":self.coupon_form})



class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        order=Order.objects.create(user=request.user)
        cart=Cart(request)
        for item in cart:
            OrderItem.objects.create(order=order, product=item["product"], quantity=item["quantity"], price=item['price'])

        return redirect("orders:order_detail", order.id)

class CouponApplyView(LoginRequiredMixin,View):
    def post(self, request, order_id):
        now=datetime.datetime.now()
        form =CouponApplyForm(request.POST)
        if form.is_valid():
            code=form.cleaned_data["code"]

        try:
            coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, "this coupon does not exist", 'danger')
            return redirect("orders:order_detail", order_id)

        order=Order.objects.get(id=order_id)
        order.discount=coupon.discount
        order.save()
        return redirect("orders:order_detail", order_id)






