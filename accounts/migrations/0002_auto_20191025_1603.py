# Generated by Django 2.2.6 on 2019-10-25 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('AG', 'Agent'), ('ST', 'Staff'), ('AD', 'Admin')], default='NU', max_length=2),
        ),
    ]
