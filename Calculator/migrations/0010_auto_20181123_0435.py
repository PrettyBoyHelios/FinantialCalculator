# Generated by Django 2.1.3 on 2018-11-23 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calculator', '0009_alternative_earnings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alternative',
            name='operative_costs',
            field=models.CharField(default='0.00', max_length=300),
        ),
    ]
