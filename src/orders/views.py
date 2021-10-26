from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer


class OrderAPIView(RetrieveAPIView, CreateAPIView, DestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        elif self.request.method == 'POST':
            return OrderItemSerializer

    def get_queryset(self):
        user = self.request.user
        self.queryset = Order.objects.all()
        return super().get_queryset().get_or_create(profile=user.profile)[-2]

    def get_object(self):
        return self.get_queryset()
