# Generated by Django 4.2.7 on 2023-12-07 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_alter_ticket_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='issue_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to='tickets.tickettype'),
        ),
    ]
