# Generated by Django 2.2.5 on 2019-10-10 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calcons', '0002_auto_20191010_0107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardealerbonus',
            old_name='bonus_percent',
            new_name='bonus_amount',
        ),
    ]
