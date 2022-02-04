from django.urls import path

from .views import order_create, order_history, order_history_detail

urlpatterns = [
    path('create/', order_create, name='order-create'),
    path('history/', order_history, name='order-history'),
    path('history/detail/<int:order_id>/',
         order_history_detail, name='order-detail'),
]

