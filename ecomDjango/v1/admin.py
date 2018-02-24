# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from v1.models import *
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('price','status','realShippingPrice','predictedShippingPrice','address')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('price','name','dimensions','weight')    