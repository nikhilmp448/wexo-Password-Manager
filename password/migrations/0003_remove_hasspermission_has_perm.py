# Generated by Django 4.1.2 on 2022-10-12 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('password', '0002_hasspermission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hasspermission',
            name='has_perm',
        ),
    ]
