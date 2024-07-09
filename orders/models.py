from django.db import models
from django.conf import settings

from products.models import Product

STATUS_CHOICES = {'pend': 'pending',
                  'deliv': 'delivered',
                  'prog': 'in progress'
                  }

# Create your models here.
class Order(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    products = models.ManyToManyField(Product)
    total_cost = models.FloatField()
    status = models.TextChoices(STATUS_CHOICES)
    