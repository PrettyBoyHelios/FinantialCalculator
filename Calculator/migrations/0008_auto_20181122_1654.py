# Generated by Django 2.1.3 on 2018-11-22 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calculator', '0007_alternative_n_periods'),
    ]

    operations = [
        migrations.AddField(
            model_name='alternative',
            name='investment',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=11),
        ),
        migrations.AddField(
            model_name='alternative',
            name='investment_payback',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=4),
        ),
    ]