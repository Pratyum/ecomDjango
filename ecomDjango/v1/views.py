# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from v1.models import *
import json
from django.core import serializers
from django.contrib.auth import authenticate
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