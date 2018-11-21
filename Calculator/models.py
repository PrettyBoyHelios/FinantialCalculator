from django.db import models
from django.forms import ModelForm

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
