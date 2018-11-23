from django.db import models
from django.forms import ModelForm
import numpy as np

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
        fields = ['name', 'description', 'interest', 'interest_type', 'n_periods', 'investment', 'investment_payback', 'earnings', 'operative_costs']


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


class Interest(models.Model):
    nominal = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    capitalizations= models.PositiveIntegerField(default=0)
    efective = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    periodic = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class InterestForm(ModelForm):
    class Meta:
        model = Interest
        fields = ['nominal', 'capitalizations','efective', 'periodic']


