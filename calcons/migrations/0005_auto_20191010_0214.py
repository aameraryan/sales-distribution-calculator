# Generated by Django 2.2.5 on 2019-10-10 02:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcons', '0004_auto_20191010_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duration',
            name='min_value',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1)]),
        ),
    ]