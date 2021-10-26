from django.db import models

from user.models import Profile
from catalog.models import Module


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.profile) + " order | created at: " + str(self.created_at)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    module = models.ForeignKey(Module, on_delete=models.PROTECT, related_name='order_module')

    def __str__(self):
        return str(self.order.profile) + ' | ' + self.module.course.name + ' - ' + self.module.name
