from django.db import models

# Create your models here.
class Product(models.Model):
    """Model definition for Product."""
    id = models.AutoField(primary_key = True)
    name = models.CharField('Name of Product', max_length=150, unique=True, blank=False, null=False)
    price = models.FloatField('Price of Product',default=0)
    stock = models.IntegerField('Stock of Product',default=0 )
    state = models.BooleanField('Estado',default = True)
    
    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return self.name
        