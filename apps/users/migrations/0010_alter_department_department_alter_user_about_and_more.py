# Generated by Django 5.0.1 on 2024-01-10 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department',
            field=models.CharField(blank=True, default='Test', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, default='Test', max_length=1500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.CharField(blank=True, default='Test', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='job',
            field=models.CharField(blank=True, default='Test', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='linkedin',
            field=models.URLField(blank=True, default='Test', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, default='Test', max_length=50),
            preserve_default=False,
        ),
    ]
