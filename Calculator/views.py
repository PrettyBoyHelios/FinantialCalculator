from django.shortcuts import render
from django.http import HttpResponse
from Calculator.models import ConversionForm, AlternativeForm, Alternative, Conversion, InterestForm, Interest
import numpy as np
import simplejson as json
from .util import get_data, clean_data
# Create your views here.

def index(request):
    return render(request, "Calculator/index.html")


def compare(request):
    altList = Alternative.objects.filter(is_selected=True)
    qty_alts = len(altList)

    # arrays for calculated properties
    if qty_alts>0:
        vnas = np.zeros(qty_alts)
        pmts = np.zeros(qty_alts)

        # n_periods validation
        prev_n = altList[0].n_periods
        flag_n = True # number of perods is the same for all alternatives

        # if all n's are equal
        for i, alt in enumerate(altList):
            print(float(alt.interest))
            if alt.n_periods != prev_n and flag_n:
                flag_n = False # any element is different
            vnas[i] = np.npv(float(alt.interest)/100, get_data(alt)) #it is already total vna
            pmts[i] = np.pmt(float(alt.interest)/100, alt.n_periods, vnas[i])

        res = list()
        indices = list()
        if flag_n:
            res = np.sort(vnas)
            indices = np.argsort(vnas)
        else:
            res = np.sort(pmts)
            indices = np.argsort(pmts)
        res = res[indices]

        altList = [alt for alt in altList]
        #altList = altList[indices]

        orderedAltList = [altList[x] for x in indices]
        best = Alternative()
        if(len(altList)>0):
            best = altList[indices[0]]
        context = {'alts': altList, 'idx': indices, 'best': best, 'qty':len(altList)}
    else:
        context = {'qty': 0}
    return render(request, "Calculator/compare.html", context)

def select_for_compare(request, id):
    # select item by id
    alternative = Alternative.objects.get(pk=id)
    alternative.is_selected = True;
    alternative.save()
    return alternatives_list(request)

def unselect_for_compare(request, id):
    #unselect item by id
    alternative = Alternative.objects.get(pk=id)
    alternative.is_selected = False
    alternative.save()
    return alternatives_list(request)

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
            alternative.earnings = clean_data(alternative.earnings)
            alternative.operative_costs = clean_data(alternative.operative_costs)
            alternative.save()
            return alternatives_list(request)
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
