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
    name = models.CharField(max_length=50, default='Test')
    interest = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    interest_type = models.CharField(max_length=10, choices=INTEREST_TYPE, default='nominal')
    operative_costs = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)


class AlternativeForm(ModelForm):
    interest = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)

    class Meta:
        model = Alternative
        fields = ['name', 'interest','interest_type', 'operative_costs']


class Conversion(models.Model):
    interest = models.DecimalField(max_digits=9, decimal_places=2)
    number_periods = models.PositiveIntegerField()
    present_value = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    future_value = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    payment = models.DecimalField(max_digits=9, decimal_places=2, blank=True)

    def calculate_values_given_future(self):
        self.present_value = self.future_value * (1 + self.interest / 100) ** (-self.number_periods)
        self.payment = self.future_value * (self.interest / 100 / ((1 + self.interest) ** self.interest - 1))

    def calculate_values_given_payment(self):
        self.present_value = self.payment * ((1 + self.interest / 100) ** self.number_periods - 1) / \
                             (self.interest * (1 + self.interest / 100) ** self.number_periods)
        self.future_value = self.payment * ((1 + self.interest / 100) ** self.number_periods - 1) / self.interest / 100

    def calculate_values_given_present(self):
        self.payment = self.present_value * (self.interest * (1 + self.interest / 100) ** self.number_periods) /\
                       ((1 + self.interest / 100) ** self.number_periods - 1)
        self.future_value = self.present_value * (1 + self.interest / 100) ** self.number_periods


class ConversionForm(ModelForm):
    class Meta:
        model = Conversion
        fields = ['interest', 'number_periods', 'present_value', 'future_value', 'payment']
