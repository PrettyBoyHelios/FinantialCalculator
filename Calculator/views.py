from django.shortcuts import render
from django.http import HttpResponse
from Calculator.models import AlternativeForm, Alternative, InterestForm, Interest
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
    if request.method == 'GET':
        form = InterestForm()
        return render(request, "Calculator/interest.html", {'form': form})
    else:
        form = InterestForm(request.POST)
        if form.is_valid():
            int_form = form.save(commit=False)
            int_form.save()
            return interest_showconversions(request)
        else:
            return HttpResponse("Invalid form")


def interest_showconversions(request):
    form = InterestForm()
    return render(request, "Calculator/show_interest.html", {'form': form})


def conversions(request):
    return render(request, "Calculator/conversions.html")
