# Generated by Django 2.2.4 on 2019-08-11 19:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20190810_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('product_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.Products')),
                ('principle_1', models.IntegerField(default=0)),
                ('principle_2', models.IntegerField(default=0)),
                ('principle_3', models.IntegerField(default=0)),
                ('principle_4', models.IntegerField(default=0)),
                ('principle_5', models.IntegerField(default=0)),
                ('principle_6', models.IntegerField(default=0)),
                ('principle_7', models.IntegerField(default=0)),
                ('principle_8', models.IntegerField(default=0)),
                ('principle_9', models.IntegerField(default=0)),
                ('principle_10', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='products',
            name='added_date',
            field=models.DateField(default=datetime.date(2019, 8, 11)),
        ),
    ]