# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from v1.models import *
import json
from django.core import serializers
from django.contrib.auth import authenticate
from utilities import get_ratio_and_savings
from django.views.decorators import csrf
# Create your views here.


class GetOrders(View):
    def get(self, request):
        orders = Order.objects.all()
        data = serializers.serialize('json',orders)
        return JsonResponse({"data":data})


class AuthenticateView(View):
    def post(self, request):
        username =  request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            data = serializers.serialize('json',user)
            return JsonResponse({"user":user,"success":True})
        else:
            return JsonResponse({"success":False,"fail-text":"Not a user"})

class CollatedOrders(View):
    def post(self, request):
        orderids = json.loads(request.POST['orderids'])
        origin_postal_code = '437934'
        destination_postal_code = request.POST['destination_postal_code']
        # for oid in orderids:
        orders = Order.objects.filter(pk=orderids)
        items_arr = []
        for order in orders:
            items = order.items
            for item in items:
                item_dict = {item.weight, item.height, item.width, item.length}
                items_arr.append(item_dict)
                print("items_arr[0]", items_arr[0])
        blitzkreig_prices_premium, individual_prices_cheap, individual_prices_premium = get_ratio_and_savings(origin_postal_code, destination_postal_code, items_arr)
        print("blitzkreig_prices_premium", blitzkreig_prices_premium)
        print("individual_prices_cheap", individual_prices_cheap)
        print("individual_prices_premium", individual_prices_premium)
