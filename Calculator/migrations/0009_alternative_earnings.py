# Generated by Django 2.1.3 on 2018-11-22 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calculator', '0008_auto_20181122_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='alternative',
            name='earnings',
            field=models.CharField(default='0.00', max_length=300),
        ),
    ]