# Generated by Django 2.2.6 on 2019-10-24 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0010_auto_20191020_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='status',
            field=models.CharField(choices=[('PA', 'Pending Approval'), ('AP', 'Approved'), ('CP', 'Completed'), ('DC', 'Declined')], default='CR', max_length=2),
        ),
    ]
