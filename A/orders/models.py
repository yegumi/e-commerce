from django.db import models
from accounts.models import User
from home.models import Product

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    paid=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=("paid", "-updated")

    def __str__(self):
        return f"{self.user} - {self.id }"

    def get_total_cost(self):
        return f"{sum(item.get_cost() for item in self.order_item.all())}"



class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order")
    quantity=models.IntegerField()
    price=models.FloatField(default=1)

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.quantity * self.price
