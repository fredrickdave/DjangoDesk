# Generated by Django 4.2.7 on 2023-11-18 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_managers_remove_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.TextField(blank=True, choices=[('Admin', 'Administrator'), ('Agent', 'Support Agent'), ('Customer', 'Customer')], null=True),
        ),
    ]
