# Generated by Django 2.2.2 on 2019-07-30 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complianceform', '0003_auto_20190728_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='entries',
            name='jotform_submission_id',
            field=models.CharField(default=123, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entries',
            name='principle',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]