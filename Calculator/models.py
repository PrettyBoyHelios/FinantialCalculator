from django.db import models
from django.forms import ModelForm

# Create your models here.
INTEREST_TYPE = (
    ('period','p'),
    ('effective', 'e'),
    ('nominal','n'),
)
class Alternative(models.Model):
    name = models.CharField(max_length=50)
    interest = models.DecimalField(max_digits=4, decimal_places=2)
    interest_type = models.CharField(max_length=10, choices=INTEREST_TYPE, default='nominal')
    operative_costs = models.DecimalField(max_digits=11, decimal_places=2)


class AlternativeForm(ModelForm):
    class Meta:
        model = Alternative
        fields = ['name', 'interest','interest_type', 'operative_costs']
