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
from django.core.mail import EmailMultiAlternatives
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
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CollatedOrders, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        data = json.loads(request.GET.get('data'))
        orderids = data['orderids']
        origin_postal_code = '437934'
        destination_postal_code = data['destination_postal_code']
        print("destination_postal_codeddddd", destination_postal_code)
        # for oid in orderids:
        orders = Order.objects.filter(pk__in=orderids)
        items_arr = []
        for order in orders:
            items = order.items.all()
            print("items lengthsdafsdfasdfsadfsadfsadfasdfs", len(items))
            for item in items:
                item_dimensions = item.dimensions.replace("mm", "")
                print("item_dimensions", item_dimensions)
                item_dimensions = item_dimensions.strip().split("x")
                print("item_dimensions", item_dimensions)
                item_dict = {"weight":float(item.weight), "height":float(item_dimensions[0])/10, "width":float(item_dimensions[1])/10, "length":float(item_dimensions[2])/10}
                items_arr.append(item_dict)
                print("items_arr[0]", items_arr[0])
        blitzkreig_prices_premium, individual_prices_cheap, individual_prices_premium = get_ratio_and_savings(items_arr, origin_postal_code, destination_postal_code)
        print("blitzkreig_prices_premium", blitzkreig_prices_premium)
        print("individual_prices_cheap", individual_prices_cheap)
        print("individual_prices_premium", individual_prices_premium)
        for idx,order in enumerate(orders):
            order.realShippingPrice = individual_prices_cheap[idx]
            order.predictedShippingPrice = blitzkreig_prices_premium[idx]
            order.premiumShippingPrice = individual_prices_premium[idx]
            order.save()
            
        return JsonResponse({"success":True, "blitzkreig_prices_premium": json.dumps(blitzkreig_prices_premium), "individual_prices_cheap": json.dumps(individual_prices_cheap), "individual_prices_premium": json.dumps(individual_prices_premium)})

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

def send_email(message, toEmail, subject):
        from_email="Admin Poolz <admin@dormbuddy.sg>"
        text_content = message
        html_content = "You have been Poolzed: <a href='https://127.0.0.1:8000/dashboard/'>"+message+"</a>"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [toEmail])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return JsonResponse({"success":True})

class CreateOrderAndItemView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateOrderAndItemView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        print(request.GET)
        items = json.loads(request.GET.get('data'))
        address = request.GET.get('address')
        user = User.objects.get(pk=1)
        totalPrice = 0
        itemsArr = []
        for item in items:
            print("Item: %s"%(item))
            price = float(item['price'])
            dimensions = item['dimensions']
            name = item['name']
            weight = item['weight']
            item = Item(name=name, price=price, dimensions=dimensions,weight=weight)
            item.save()
            itemsArr.append(item)
            print("Item Added: %s" %(name))
            totalPrice = totalPrice + price
        order = Order(price=totalPrice,status="Incomplete",realShippingPrice=0.0,predictedShippingPrice=0.0,address=address) 
        order.save()
        order.userOrdered.add(user)     
        for item in itemsArr:
            order.items.add(item)      
        order.save()
        send_email("Click Here","singhpriyanshu5@gmail.com","Your order has been poolzyed")
        # send_email("Click Here","pratyum001@e.ntu.edu.sg","Your order has been poolzyed")
        send_email("Click Here","shantanukamath@live.in","Your order has been poolzyed")
        send_email("Click Here","gargutsav96@gmail.com","Your order has been poolzyed")
        # send_email("Click Here","vinithrnair@gmail.com","Your order has been poolzyed") 
        print("Order Saved: %d"%(order.id))
        return JsonResponse({"success":True,"orderID":order.id})


class SendEmailView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SendEmailView, self).dispatch(request, *args, **kwargs)

    def get(self,request):
        message=request.GET.get('message')
        to =request.GET.get('toEmail')
        subject = request.GET.get('subject')
        from_email="admin@dormbuddy.sg"
        text_content = message
        html_content = "<p>" + message + "<p>"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return JsonResponse({"success":True})


