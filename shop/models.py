from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    annual_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    stripe_price_id = models.CharField(max_length=100, null=True)  # e.g., price_abc123
    is_subscription = models.BooleanField(default=True)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name