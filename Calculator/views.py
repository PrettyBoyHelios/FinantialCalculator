from django.shortcuts import render
#from django.http import HttpRespose
from Calculator.models import AlternativeForm
# Create your views here.

def index(request):
    return render(request, "Calculator/index.html")


def alternatives_list(request):
    return render(request, "Calculator/alternatives.html")


def create_alternative(request):
    if request.method == 'GET':
        form = AlternativeForm()
        return render(request, "Calculator/create_alternative.html", {'form': form})
    else:
        pass
    return render(request, "Calculator/alternatives_list.html")


def interest_conversions(request):
    return render(request, "Calculator/interest.html")


def conversions(request):
    return render(request, "Calculator/conversions.html")
