from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def prueba(request):
    return HttpResponse("Esta es una prueba corriendo con docker.")
