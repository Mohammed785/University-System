from django.shortcuts import render
from grades.models import Grade

#TODO: exam our shit view system and re use it here

def home(request):
    return render(request,'college/home.html')
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'college/about.html')

def support(request):
    return render(request,'college/support.html')

def error_404_handler(request,exception):
    return render(request,'error/404.html')


def error_500_handler(request):
    return render(request,'error/500.html')


def error_403_handler(request,exception):
    return render(request,'error/403.html')


def error_400_handler(request,exception):
    return render(request,'error/400.html')