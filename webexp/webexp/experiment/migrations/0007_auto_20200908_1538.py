# Generated by Django 3.1 on 2020-09-08 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0006_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='page',
            field=models.IntegerField(),
        ),
    ]