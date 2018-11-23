from django.shortcuts import render
from django.http import HttpResponse
from Calculator.models import *
# Create your views here.

def index(request):
    return render(request, "Calculator/index.html")


def alternatives_list(request):
    altList = Alternative.objects.all()
    context = {'alts': altList }
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
    if request.method == 'GET':
        form = ConversionForm()
        return render(request, 'Calculator/conversions.html', {'form': form})
    else:
        form = ConversionForm(request.POST)
        if form.is_valid():
            conversion = form.save(commit=False)
            if conversion.future_value is not None:
                conversion.calculate_values_given_future()
                return render(request, 'Calculator/conversions_results.html', {
                    'conversion': conversion
                })
            elif conversion.payment is not None:
                conversion.calculate_values_given_payment()
                return render(request, 'Calculator/conversions_results.html', {
                    'conversion': conversion
                })
            elif conversion.present_value is not None:
                conversion.calculate_values_given_present()
                return render(request, 'Calculator/conversions_results.html', {
                    'conversion': conversion
                })
            else:
                return HttpResponse('Invalid data')
        else:
            return HttpResponse('Invalid form')


def number_periods(request):
    if request.method == 'GET':
        form = NumberPeriodsForm()
        return render(request, 'Calculator/number_periods.html', {'form': form})
    else:
        form = NumberPeriodsForm(request.POST)
        if form.is_valid():
            form_periods = form.save(commit=False)
            if form_periods.present_value is not None and form_periods.future_value is not None:
                periods = form_periods.calculate_periods_given_fp()
                return render(request, 'Calculator/number_periods_results.html', {
                    'periods': periods
                })
            elif form_periods.future_value is not None and form_periods.payment is not None:
                periods = form_periods.calculate_periods_given_fa()
                return render(request, 'Calculator/number_periods_results.html', {
                    'periods': periods
                })
            elif form_periods.present_value is not None and form_periods.payment is not None:
                periods = form_periods.calculate_periods_given_pa()
                return render(request, 'Calculator/number_periods_results.html', {
                    'periods': periods
                })
            else:
                return HttpResponse('Invalid Data')
        else:
            return HttpResponse('Invalid Form')

