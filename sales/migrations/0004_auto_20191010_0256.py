# Generated by Django 2.2.5 on 2019-10-10 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_auto_20191010_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='duration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calcons.Duration'),
        ),
    ]
