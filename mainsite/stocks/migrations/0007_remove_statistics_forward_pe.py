# Generated by Django 3.1.4 on 2021-01-21 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_statistics_trailing_pe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statistics',
            name='forward_pe',
        ),
    ]
