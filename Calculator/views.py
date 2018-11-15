from django.shortcuts import render
#from django.http import HttpRespose
from Calculator.models import AlternativeForm
# Create your views here.

def index(request):
    form = AlternativeForm()
    return render(request, "Calculator/index.html", {'form': form})

def alternatives_list(request):

    return render(request, "Calculator/alternatives_list.html")