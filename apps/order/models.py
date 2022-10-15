from pyexpat import model
from tkinter import CASCADE
from django.db import models

from apps.product.models import Product
# Create your models here.

class Order(models.Model):
    id = models.AutoField(primary_key = True)
    create_date = models.DateTimeField('Created date', auto_now=False, auto_now_add=True)
    modified_date = models.DateTimeField('Modified date', auto_now=True, auto_now_add=False )

    class Meta:
        ordering = ['id']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        """Unicode representation of Order."""
        return str(self.id)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order', on_delete= models.CASCADE)
    cuantity = models.IntegerField('Cuantity')
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Orders Details'


    def __str__(self):
        """Unicode representation of Order Detail."""
        return str(self.order)

