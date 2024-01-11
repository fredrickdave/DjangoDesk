# Generated by Django 4.2.7 on 2024-01-10 07:00

import apps.tickets.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0014_alter_ticketattachment_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='priority_id',
        ),
        migrations.AddField(
            model_name='ticket',
            name='priority',
            field=models.IntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default=3),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.IntegerField(choices=[(1, 'Open'), (2, 'Assigned'), (3, 'In Progress'), (4, 'On Hold'), (5, 'Resolved'), (6, 'Closed')], default=1),
        ),
        migrations.AlterField(
            model_name='ticketattachment',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to=apps.tickets.models.attachment_directory_path, validators=[apps.tickets.models.validate_file_size, apps.tickets.models.validate_file_type]),
        ),
    ]