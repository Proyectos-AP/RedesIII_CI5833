from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from sales.models import Client, Product

# Create your views here.

def index(request):
    return render(request, 'sales/index.html')

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['psw']
            user = Client(username=username,password=password)
            user.save()
            return render(request,'sales/index.html')
        except:
            return render(request,'sales/error.html')

    else:
        return render(request,'sales/register.html')

def login(request):
    if request.method == 'POST':
        return render(request,'sales/platform.html')
    else:
        return render(request,'sales/login.html')

def logout(request):
    return HttpResponse("Logout")

def platform(request):
    if request.method == 'POST':
        # Process a transaction
        print("Process a transaction")
    else:

        products_list = Product.objects.all()
        context = {
            'products_list': products_list,
            }
        return render(request,'sales/platform.html',context)
