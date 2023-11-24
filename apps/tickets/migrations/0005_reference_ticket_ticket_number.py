# Generated by Django 4.2.7 on 2023-11-24 09:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_alter_ticketpriority_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_number',
            field=models.CharField(db_index=True, default=django.utils.timezone.now, max_length=25),
            preserve_default=False,
        ),
    ]
