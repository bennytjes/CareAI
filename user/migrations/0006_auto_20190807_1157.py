# Generated by Django 2.2.4 on 2019-08-07 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20190807_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='deploy_point',
            field=models.CharField(choices=[('Primary Care', 'Primary Care'), ('Secondary Care', 'Secondary Care'), ('Community Care', 'Community Care'), ('Tertiary Care', 'Tertiary Care'), ('Individual Care of Self e.g. user’s home/office', 'Individual Care of Self e.g. user’s home/office'), ('For the purposes of population screening', 'For the purposes of population screening'), ('Other', 'Other (please specify)')], default='other', max_length=100, verbose_name='At which point of care do you expect your data-driven solution to be deployed? Select as many as applicable.'),
        ),
        migrations.AlterField(
            model_name='products',
            name='other_category',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Other category:'),
        ),
        migrations.AlterField(
            model_name='products',
            name='other_deploy_point',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Other point of care:'),
        ),
    ]
