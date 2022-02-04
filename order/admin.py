from django.contrib import admin

# Register your models here.
from .models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_filter = ['created',]
    list_display = ['id', 'address', 'created']

# admin.site.register(Order, OrderAdmin)