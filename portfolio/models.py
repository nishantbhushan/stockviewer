from django.db import models


# Create your models here.

class portfolioModel(models.Model):
    userId = models.IntegerField(verbose_name="User ID")
    ticker = models.CharField(max_length=30)
    datePurchased = models.DateField(verbose_name="Date Purchased")
    quantity = models.DecimalField(max_digits=5, decimal_places=3)
    costBasis = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='Cost Basis')
    buyType = models.CharField(max_length=30, verbose_name="Type of Buy")
    country = models.CharField(max_length=100)


class samplemodel(models.Model):
    decimalInput = models.DecimalField(max_digits=4, decimal_places=2)