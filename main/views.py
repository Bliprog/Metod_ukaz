from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.views import LoginView
from .models import *
from .forms import *
from django.views import View
from django.contrib.auth.forms import *
from django import forms
import datetime
import json
from django.http import HttpResponseRedirect, JsonResponse
from itertools import chain

def regiser (request):
    if request.method == "POST":
        form_u = CreateUserForm(request.POST)
        form_c = CreateClientForm(request.POST)
        if form_u.is_valid() and form_c.is_valid():
            form_u.save()
            Client.objects.create(user=User.objects.last(), otchestvo=form_c.cleaned_data['otchestvo'])
            return redirect('login')
        else:
            return redirect('register')
    else:
        form_u = CreateUserForm()
        form_c = CreateClientForm()
        return render(request, 'register.html', {'form_c':form_c, 'form_u':form_u})

def main(request):
    if request.user.is_authenticated:
        context={}
        if request.method == "POST":
            order = Order.objects.get(pk=request.POST['num'], client=Client.objects.get(user=request.user))
            order.state = State.objects.get(state='Отменен')
            orders_products = Orders_products.objects.filter(order=order)
            for order_prod in orders_products:
                order_prod.product.count+=order_prod.count
            order.save()
            return JsonResponse({
                'success': True
            })
        else:
            orders = Order.objects.filter(client=Client.objects.get(user=request.user), is_created=True)
            context['orders']=orders
            chai = chain()
            for order in orders:
                count_prod =Orders_products.objects.filter(order=order)
                chai=chain(chai,count_prod)
            context['order_products'] = list(chai)
            print(context['order_products'])
            return render(request,'main.html', context)
    else: return redirect('login/')

def create_order(request):
    if request.user.is_authenticated:
        order = Order.objects.get_or_create(client=Client.objects.get(user=request.user), manager=Manager.objects.last(), is_created=False, defaults={'state':State.objects.get(state='В сборке'), 'date_create':datetime.datetime.now().date(), 'time_create':datetime.datetime.now().time})
        if order[1]==True:
            order[0].manager.count_orders += 1
            order[0].manager.save()
        order = order[0]
        if request.method=="GET":
            products = Product.objects.all()
            context={}
            context['products']=products
            orders_product = Orders_products.objects.filter(order=order)
            sum = 0
            for op in orders_product:
                sum+=op.product.price_p * op.count
            context['sum']=sum
            context['order_products'] = orders_product
            return render(request,'create_order.html',context)
        if request.method=='POST':
            if request.POST['type']=='add_p':
                product = Product.objects.get(pk=request.POST['num'])
                count=request.POST['count']
                if count !='':
                    orders_product = Orders_products.objects.get_or_create(order=order, product=product,defaults={'count': count})
                    if(orders_product[1]==False):
                        orders_product[0].count += int(count)
                        orders_product[0].save()
            elif request.POST['type']=='delete_p':
                product = Product.objects.get(pk=request.POST['num'])
                count = request.POST['count']
                orders_product = Orders_products.objects.get(order=order, product=product)
                if int(count)<orders_product.count:
                    orders_product.count -= int(count)
                    orders_product.save()
                else:
                    orders_product.delete()
            elif request.POST['type']=='confirm_order' and Orders_products.objects.filter(order=order).exists():
                order.is_created=True
                orders_products = Orders_products.objects.filter(order=order)
                for order_prod in orders_products:
                    if order_prod.product.count >= order_prod.count:
                        order_prod.product.count-=order_prod.count
                        order_prod.product.save()
                    else:
                        order_prod.count=order_prod.product.count
                        order_prod.save()
                        order_prod.product.count=0
                        order_prod.product.save()
                order.save()
            return JsonResponse({
                'success': True
            })

    else:
        return redirect('login')

def otchet_sells(request):
    if request.user.is_authenticated:
        if request.method=='GET':
           form = DateForm()
           return render(request,'O_sells.html',{'form':form, 'is_otchet':False})
        elif request.method == 'POST':
            form = DateForm(request.POST)
            context = {}
            if(form.is_valid()):
                print('why')
                date_s = form.cleaned_data['date_start']
                date_e = form.cleaned_data['date_end']
                orders = Order.objects.filter(date_create__range=(date_s,date_e), state=State.objects.get(state='Завершен'))
                sum = 0
                context['count_orders']=orders.count()
                prod_l=[]
                for product in Product.objects.all():
                    prod = {}
                    prod['code_product']=product.pk
                    prod['count']=0
                    prod['price']=product.price_p
                    prod['name']=product.creator.name +' '+product.name
                    for order in orders:
                        products_order = Orders_products.objects.filter(order=order)
                        for order_product in products_order:
                            if order_product.product == product:
                                prod['count']+=order_product.count
                    prod['sum']=prod['price']*prod['count']
                    sum+=prod['sum']
                    prod_l.append(prod)
                context['all_sum']=sum
                context['products']=prod_l
                context['is_otchet']=True
                print(context)
            context['form'] = form
            return render(request, 'O_sells.html', context)
    else:
        return redirect('login')

def otchet_cancels(request):
    if request.user.is_authenticated:
        if request.method=='GET':
           form = DateForm()
           return render(request,'O_sells.html',{'form':form, 'is_otchet':False})
        elif request.method == 'POST':
            form = DateForm(request.POST)
            context = {}
            if(form.is_valid()):
                print('why')
                date_s = form.cleaned_data['date_start']
                date_e = form.cleaned_data['date_end']
                orders = Order.objects.filter(date_create__range=(date_s,date_e), state=State.objects.get(state='Отменен'))
                context['count_orders']=orders.count()
                context['is_otchet']=True
            context['form'] = form
            return render(request, 'O_cancels.html', context)
    else:
        return redirect('login')

def otchet_products(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            context={}
            context['products'] = Product.objects.all()
            return render(request, 'O_products.html', context)
    else:
        return redirect('login')
