# Generated by Django 2.2 on 2020-04-20 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_usercard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercard',
            name='cadr_last4_digit',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='usercard',
            name='exp_month',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='usercard',
            name='exp_year',
            field=models.IntegerField(),
        ),
    ]
