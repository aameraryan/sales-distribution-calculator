# Generated by Django 2.2.6 on 2019-10-25 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_auto_20191017_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('PN', 'Pending'), ('SL', 'Solved'), ('CN', 'Cancelled')], default='IN', max_length=2),
        ),
    ]
