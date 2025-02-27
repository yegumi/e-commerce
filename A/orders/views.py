from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        items = []
        total_cost=0
        for product_id, item_data in cart.cart.items():
            product = Product.objects.filter(id=product_id).first()
            if product:
                item_total_price=item_data['quantity'] * float(item_data['price'])
                item = {
                    'product': product,  # Pass the full product object
                    'quantity': item_data['quantity'],
                    'price': item_data['price'],
                    'total_price': item_total_price,
                }
                total_cost += item_total_price
                items.append(item)

        return render(request, 'orders/cart.html', {'items': items,"total_cost":total_cost})


class CartAddView(View):
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
    def get(self, request, order_id):
        order=get_object_or_404(Order,id=order_id)
        return render(request, "orders/order.html", {"order":order})



class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        order=Order.objects.create(user=request.user)
        cart=Cart(request)
        for item in cart:
            OrderItem.objects.create(order=order, product=item["product"], quantity=item["quantity"], price=item['price'])
        cart.clear()

        return redirect("orders:order_detail", order.id)

