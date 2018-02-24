# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Order(models.Model):
    PROGRESS_STATUS_OPTIONS = (
        ('I', 'Incomplete'),
        ('P', 'In Progress'),
        ('C', 'Complete'),
    )
    price = models.DecimalField(max_digits=20,decimal_places=2)
    status = models.CharField(max_length=1, choices=PROGRESS_STATUS_OPTIONS)
    realShippingPrice = models.DecimalField(max_digits=10,decimal_places=2)
    predictedShippingPrice = models.DecimalField(max_digits=10,decimal_places=2)
    userOrdered = models.ManyToManyField(
        User
    )
    address = models.TextField()

class Item(models.Model):
    price = models.DecimalField(max_digits=20,decimal_places=2)
    name = models.CharField(max_length=100)
    dimensions = models.CharField(max_length=40)
    weight = models.DecimalField(max_digits=6,decimal_places=2)
    referenceOrder = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
    )