# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Item(models.Model):
    price = models.DecimalField(max_digits=20,decimal_places=2)
    name = models.CharField(max_length=100)
    dimensions = models.CharField(max_length=40)
    weight = models.DecimalField(max_digits=6,decimal_places=2)

class Order(models.Model):
    PROGRESS_STATUS_OPTIONS = (
        ('Incomplete', 'Incomplete'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
    )
    price = models.DecimalField(max_digits=20,decimal_places=2)
    status = models.CharField(max_length=15, choices=PROGRESS_STATUS_OPTIONS)
    realShippingPrice = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    premiumShippingPrice = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    predictedShippingPrice = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    userOrdered = models.ManyToManyField(User, blank=True)
    address = models.TextField()
    items = models.ManyToManyField(Item,blank=True)

