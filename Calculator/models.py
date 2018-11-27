from django.db import models
from django.forms import ModelForm
from django import forms
import decimal
import numpy as np
import locale
# Create your models here.
INTEREST_TYPE = (
    ('p', 'period'),
    ('e', 'effective'),
    ('n', 'nominal'),
)


class Alternative(models.Model):
    is_selected = models.BooleanField(default=False)
    name = models.CharField(max_length=50, default='Test')
    description = models.TextField(max_length=200, default="")
    interest = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    interest_type = models.CharField(max_length=10, choices=INTEREST_TYPE, default='nominal')
    n_periods = models.PositiveIntegerField(default=1)
    investment = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    investment_payback = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    earnings = models.CharField(max_length=300, default='0.00')
    operative_costs = models.CharField(max_length=300, default='0.00')


class AlternativeForm(ModelForm):
    interest = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)

    class Meta:
        model = Alternative
        fields = ['name', 'description', 'interest', 'n_periods', 'investment', 'investment_payback', 'earnings', 'operative_costs']
        labels = {
            'name':'Project\'s Name',
            'description': 'Description',
            'interest': 'TREMA',
            'n_periods': 'Number of Periods',
            'earnings': 'Income',
            'operative_costs': 'Expenses',
            'investment_payback': 'Investment Payback (%)',

        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'investment_payback': forms.NumberInput(attrs={'step': 0.1}),
        }


class Conversion(models.Model):
    interest = models.DecimalField(max_digits=9, decimal_places=2)
    number_periods = models.PositiveIntegerField()
    present_value = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    future_value = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    payment = models.DecimalField(max_digits=9, decimal_places=2, blank=True)

    def calculate_values_given_future(self):
        self.present_value = self.future_value * (1 + self.interest / 100) ** (-self.number_periods)
        self.payment = self.future_value * (self.interest / 100 / ((1 + self.interest / 100) ** self.number_periods - 1))

    def calculate_values_given_payment(self):
        self.present_value = self.payment * ((1 + self.interest / 100) ** self.number_periods - 1) / \
                             (self.interest * (1 + self.interest / 100) ** self.number_periods)
        self.future_value = self.payment * ((1 + self.interest / 100) ** self.number_periods - 1) / self.interest / 100

    def calculate_values_given_present(self):
        self.payment = self.present_value * (self.interest / 100 * (1 + self.interest / 100) ** self.number_periods) /\
                       ((1 + self.interest / 100) ** self.number_periods - 1)
        self.future_value = self.present_value * (1 + self.interest / 100) ** self.number_periods


class ConversionForm(ModelForm):
    class Meta:
        model = Conversion
        fields = ['interest', 'number_periods', 'present_value', 'future_value', 'payment']


class NumberPeriods(models.Model):
    interest = models.DecimalField(max_digits=9, decimal_places=2)
    present_value = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    future_value = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    payment = models.DecimalField(max_digits=9, decimal_places=2, blank=True)

    def calculate_periods_given_fp(self):
        return np.ceil(np.log(float(self.future_value / self.present_value)) / np.log(float(1 + self.interest / 100)))

    def calculate_periods_given_fa(self):
        return np.ceil(np.log(float(1 + self.interest / 100 * (self.future_value / self.payment))) / np.log(float(1 + self.interest / 100)))

    def calculate_periods_given_pa(self):
        return np.ceil(-np.log(float(1 - self.interest / 100 * (self.present_value / self.payment))) / np.log(float(1 + self.interest / 100)))


class NumberPeriodsForm(ModelForm):
    class Meta:
        model = NumberPeriods
        fields = ['interest', 'present_value', 'future_value', 'payment']


class Interest(models.Model):

    nominal = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    capitalizations= models.PositiveIntegerField(blank=True)
    efective = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    periodic = models.DecimalField(max_digits=9, decimal_places=2, blank=True)

    def R_M(self):
        # teniendo r y m
        campoR=self.nominal
        campoM=self.capitalizations
        interesNominal = campoR /100
        n_capitalizaciones = campoM
        intEfectivo = ((1 + (interesNominal / n_capitalizaciones)) ** n_capitalizaciones) - 1
        intPeriodo = interesNominal / n_capitalizaciones
        self.efective = intEfectivo*100
        self.periodic = intPeriodo*100

    def IP_M(self):
        # teniendo ip y m
        campoIP = self.periodic
        campoM=self.capitalizations
        intPeriodo = campoIP /100
        n_capitalizaciones = campoM
        interesNominal = intPeriodo * n_capitalizaciones
        intEfectivo = ((1 + (interesNominal / n_capitalizaciones)) ** n_capitalizaciones) - 1
        self.nominal = interesNominal*100
        self.efective = intEfectivo*100


    def R_IP(self):
        # teniendo r & ip
        campoR=self.nominal
        campoIP=self.periodic
        interesNominal = campoR /100
        intPeriodo = campoIP /100
        n_capitalizaciones = interesNominal / intPeriodo
        intEfectivo = ((1 + (interesNominal / n_capitalizaciones)) ** n_capitalizaciones) - 1
        self.efective = intEfectivo*100
        self.capitalizations = interesNominal/intPeriodo

    def M_IEF(self):
        # teniendo m & ief
        campoM=self.capitalizations
        campoIEF=self.efective
        n_capitalizaciones = campoM
        intEfectivo = campoIEF /100
        interesNominal = (decimal.Decimal((intEfectivo + 1)) ** decimal.Decimal((1 / n_capitalizaciones)) - 1) * n_capitalizaciones
        intPeriodo = interesNominal / n_capitalizaciones
        self.nominal=interesNominal*100
        self.periodic = intPeriodo*100


class InterestForm(ModelForm):
    class Meta:
        model = Interest
        fields = ['nominal', 'capitalizations', 'efective', 'periodic']


class ViewAlternativeResult:
    def __init__(self, alternative, vna, pmt, irr):
        locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')
        self.alt = alternative
        self.vna = locale.currency(round(vna, 2), grouping=True)
        self.pmt = locale.currency(round(pmt, 2), grouping=True)
        self.pk = alternative.pk
        if irr == np.nan:
            self.irr = None
        else:
            self.irr = round(irr, 2)



