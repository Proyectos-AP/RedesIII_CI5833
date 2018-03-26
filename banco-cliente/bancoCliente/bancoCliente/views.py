from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


# Create your views here.
def index(request):
    return render(request, 'bancoCliente/index.html')