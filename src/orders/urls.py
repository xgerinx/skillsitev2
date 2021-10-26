from django.urls import path

from orders.views import OrderAPIView

urlpatterns = [
    path('cart/', OrderAPIView.as_view(), name='cart'),
]
