from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInlines(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("product", )
    # Use raw_id_fields to show a text input for the 'product' field instead of selecting its id


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "paid", "updated")
    list_filter = ("paid", )
    inlines = (OrderItemInlines,)

