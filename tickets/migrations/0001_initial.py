# Generated by Django 2.2.5 on 2019-09-29 00:21

from django.db import migrations, models
import django.db.models.deletion
import tickets.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.CharField(default=tickets.models.ticket_id_generator, max_length=32)),
                ('status', models.CharField(choices=[('IN', 'Initiated'), ('PR', 'Processing'), ('SL', 'Solved'), ('CN', 'Cancelled'), ('EX', 'Expired')], default='IN', max_length=2)),
                ('query_type', models.CharField(choices=[('PR', 'Price'), ('PM', 'Payment'), ('OT', 'Other')], default='OT', max_length=2)),
                ('description', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='tickets/photos/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('solved_on', models.DateTimeField(blank=True, null=True)),
                ('executive_description', models.TextField(blank=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
        ),
    ]
