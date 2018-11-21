from django.shortcuts import render
from django.http import HttpResponse
from Calculator.models import AlternativeForm, Alternative
# Create your views here.

def index(request):
    return render(request, "Calculator/index.html")


def alternatives_list(request):
    altList = Alternative.objects.all()
    context = { 'alts':altList }
    return render(request, "Calculator/alternatives.html", context)


def create_alternative(request):
    if request.method == 'GET':
        form = AlternativeForm()
        return render(request, "Calculator/create_alternative.html", {'form': form})
    else:
        form = AlternativeForm(request.POST)
        if form.is_valid():
            alternative = form.save(commit=False)
            alternative.save()
            return render(request, "Calculator/alternatives.html")
        else:
            return HttpResponse("Invalid form")



def interest_conversions(request):
    return render(request, "Calculator/interest.html")


def conversions(request):
    return render(request, "Calculator/conversions.html")
