# Generated by Django 2.2.2 on 2019-07-28 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complianceform', '0002_formurls'),
    ]

    operations = [
        migrations.CreateModel(
            name='JotFormIDs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('principle', models.IntegerField()),
                ('jotform_id', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='FormURLs',
        ),
    ]