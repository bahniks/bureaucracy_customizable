# Generated by Django 3.1 on 2020-09-15 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0009_auto_20200915_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='gets',
        ),
    ]
