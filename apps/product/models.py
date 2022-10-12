from django.db import models

# Create your models here.
class Product(models.Model):
    """Model definition for Product."""
    id = models.CharField(primary_key = True, max_length=1000)
    name = models.CharField('Name of Product', max_length=150, unique=True, blank=False, null=False)
    price = models.FloatField('Price of Product',default=0)
    stock = models.IntegerField('Stock of Product',default=0 )

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return self.name