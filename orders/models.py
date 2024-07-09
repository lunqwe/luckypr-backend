from django.db import models
from django.conf import settings

from products.models import Product


class Status(models.TextChoices):
        PENDING = 'pend', 'Pending'
        DELIVERED = 'deliv', 'Delivered'
        IN_PROGRESS = 'prog', 'In Progress'

# Create your models here.
class Order(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default="Anonymous user")
    products = models.ManyToManyField(Product)
    total_cost = models.FloatField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    deliver_to = models.CharField(max_length=999)
    