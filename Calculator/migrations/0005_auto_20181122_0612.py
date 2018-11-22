# Generated by Django 2.1.3 on 2018-11-22 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calculator', '0004_interest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.DecimalField(decimal_places=2, max_digits=9)),
                ('number_periods', models.PositiveIntegerField()),
                ('present_value', models.DecimalField(blank=True, decimal_places=2, max_digits=9)),
                ('future_value', models.DecimalField(blank=True, decimal_places=2, max_digits=9)),
                ('payment', models.DecimalField(blank=True, decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.AddField(
            model_name='alternative',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
    ]