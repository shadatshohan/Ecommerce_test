# Generated by Django 3.2.8 on 2021-10-31 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_auto_20211031_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
    ]
