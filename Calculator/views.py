from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from Calculator.models import *
import numpy as np
import simplejson as json
from .util import get_data, clean_data


def index(request):
    return render(request, "Calculator/index.html")


def compare(request):
    altList = Alternative.objects.filter(is_selected=True)
    qty_alts = len(altList)

    # arrays for calculated properties
    if qty_alts>0:
        vnas = np.zeros(qty_alts)
        pmts = np.zeros(qty_alts)
        irr = np.zeros(qty_alts)

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
            irr[i] = np.irr(get_data(alt))
        print(flag_n,irr, get_data(alt))

        res = list()
        indices = list()
        if flag_n:
            indices = np.argsort(vnas)
            #res = np.sort(vnas)
        else:
            indices = np.argsort(pmts)
            #res = np.sort(pmts)

        print('idx', indices)
        #res = res[indices]
        #irr = irr[indices]
        altList = [alt for alt in altList]
        for alt in altList:
            print(alt.name)
        #orderedAltList = [altList[x] for x in indices]
        viewList = [ViewAlternativeResult(altList[i], vnas[i], pmts[i], irr[i]) for i in range(qty_alts)]

        for alr in viewList:
            print(alr.alt.earnings)
        best = viewList[0]
        # if len(altList)>0:
        #     best = altList[indices[0]]
        context = {'alts': viewList, 'best': best, 'qty': len(altList)}
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


def edit_alternative(request, id):
    print(request.method)
    model = get_object_or_404(Alternative, pk=id)
    if request.method == 'GET':

        print(model)
        form = AlternativeForm(instance=model)
        header = 'Edit Alternative'
        action_str = ' Save'
        return render(request, "Calculator/create_alternative.html", {'form': form, 'header': header, 'action_str': action_str, 'edit': True, 'mod_id': model.pk })
    else:
        form = AlternativeForm(request.POST)
        if form.is_valid():
            alternative = form.save(commit=False)
            alternative.pk = id
            alternative.earnings = clean_data(alternative.earnings)
            alternative.operative_costs = clean_data(alternative.operative_costs)
            alternative.save()
            return alternatives_list(request)
        else:
            return HttpResponse("Invalid form")


def create_alternative(request):
    if request.method == 'GET':
        form = AlternativeForm()
        header = ' Create Alternative'
        action_str = ' Create'
        return render(request, "Calculator/create_alternative.html", {'form': form, 'header': header, 'action_str': action_str, 'edit': False })
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
            Error = False
            if int_form.nominal is not None:
                if int_form.capitalizations is not None and int_form.capitalizations <= 365:
                    int_form.R_M()
                    return render(request, 'Calculator/show_interest.html', {'data': int_form})
                elif int_form.periodic is not None:
                    int_form.R_IP()
                    return render(request, 'Calculator/show_interest.html', {'data': int_form})
                else:
                    Error=True
            elif int_form.capitalizations is not None and int_form.capitalizations <= 365:
                if int_form.periodic is not None:
                    int_form.IP_M()
                    return render(request, 'Calculator/show_interest.html', {'data': int_form })
                elif int_form.efective is not None:
                    int_form.M_IEF()
                    return render(request, 'Calculator/show_interest.html', {'data': int_form})
                else:
                    Error=True
            else:
                Error=True
        else:
            return render(request, 'Calculator/interest_formerror.html')
        if Error:
            return render(request, 'Calculator/interest_error.html')


def interest_showconversions(request):
    return render(request, "Calculator/show_interest.html")


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
                return render(request, 'Calculator/conversions_error.html')
        else:
            return render(request, 'Calculator/conversions_formerror.html')


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
                return render(request, 'Calculator/number_periods_error.html')
        else:
            return render(request, 'Calculator/number_periods_formerror.html')

