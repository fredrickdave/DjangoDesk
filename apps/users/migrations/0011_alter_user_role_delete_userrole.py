# Generated by Django 5.0.1 on 2024-01-10 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_department_department_alter_user_about_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'Administrator'), (2, 'Support Agent'), (3, 'Customer')], default=3),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='UserRole',
        ),
    ]
