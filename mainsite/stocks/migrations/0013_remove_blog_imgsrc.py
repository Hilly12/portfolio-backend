# Generated by Django 3.1.4 on 2021-06-15 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0012_auto_20210615_2324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='imgSrc',
        ),
    ]