# Generated by Django 2.2.4 on 2019-08-15 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20190811_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='audited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='products',
            name='added_date',
            field=models.DateField(default=datetime.date(2019, 8, 15)),
        ),
    ]