from django.db import models

# Create your models here.
INTEREST_TYPE = (
    ('period','p'),
    ('effective', 'e'),
    ('nominal','n'),
)
class Alternative(models.Model):
    interest = models.DecimalField(max_digits=4, decimal_places=2)
    interest_type = models.CharField(max_length=10, choices=INTEREST_TYPE, default='nominal')

