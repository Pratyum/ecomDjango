# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from v1.models import *
import json
from django.core import serializers
from utilities import get_ratio_and_savings
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
# Create your views here.


class GetOrders(View):
    def get(self, request):
        jsonToSend = {}
        orders = Order.objects.all()
        items = Item.objects.all()
        dataOrders = serializers.serialize('json',orders)
        dataItems = serializers.serialize('json',items)
        return JsonResponse({"orders":dataOrders,"items":dataItems})


class AuthenticateView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthenticateView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        username =  request.POST['username']
        password = request.POST['password']
        print("Username:%s , Password: %s " % (username,password))
        user = authenticate(username=username, password=password)
        if user is not None:
            # data = serializers.serialize('json',user)
            login(request,user)
            return JsonResponse({"success":True})
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

class SignUpView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        username =  request.POST['username']
        password = request.POST['password']
        print("Username:%s , Password: %s " % (username,password))
        user = authenticate(username=username, password=password)
        if user is not None:
            # data = serializers.serialize('json',user)
            login(request,user)
            return JsonResponse({"success":True})
        else:
            return JsonResponse({"success":False,"fail-text":"Not a user"})


class DashboardView(TemplateView):
    template_name = "v1/dashboard.html"

class OrderHistoryView(ListView):
    template_name = "v1/history.html"
    model = Order

class SignInWebView(TemplateView):
    template_name = "v1/login.html"

class SignUpWebView(TemplateView):
    template_name = "v1/signup.html"
