# Generated by Django 2.2.4 on 2019-08-10 17:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20190807_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='added_date',
            field=models.DateField(default=datetime.date(2019, 8, 10)),
        ),
    ]
