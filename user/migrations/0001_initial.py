# Generated by Django 2.2.4 on 2019-08-19 10:17

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(default='product name', max_length=100)),
                ('added_date', models.DateField(default=datetime.date(2019, 8, 19))),
                ('category', models.CharField(choices=[('Diagnostic', 'Diagnostic'), ('Therapeutic', 'Therapeutic'), ('Population health', 'Population health'), ('Care-based', 'Care-based'), ('Triage', 'Triage'), ('Self-care', 'Self-care'), ('Health promotion', 'Health promotion'), ('Remote Monitoring', 'Remote Monitoring'), ('Remote Consultation', 'Remote Consultation'), ('Other', 'Other (please specify)')], max_length=30)),
                ('other_category', models.CharField(blank=True, max_length=30, null=True, verbose_name='Other category:')),
                ('deploy_point', user.models.MSF(choices=[('Primary Care', 'Primary Care'), ('Secondary Care', 'Secondary Care'), ('Community Care', 'Community Care'), ('Tertiary Care', 'Tertiary Care'), ('Individual Care of Self e.g. user’s home/office', 'Individual Care of Self e.g. user’s home/office'), ('For the purposes of population screening', 'For the purposes of population screening'), ('Other', 'Other (please specify)')], default='other', max_length=100, verbose_name='At which point of care do you expect your data-driven solution to be deployed? Select as many as applicable.')),
                ('other_deploy_point', models.CharField(blank=True, max_length=100, null=True, verbose_name='Other point of care:')),
                ('description', models.TextField()),
                ('audited', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('user_id', models.OneToOneField(db_column='user_id', default=0, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=50, null=True)),
                ('is_supplier', models.BooleanField(default=False, verbose_name='I am a supplier')),
                ('first_name', models.CharField(max_length=20, null=True)),
                ('last_name', models.CharField(max_length=20, null=True)),
                ('organisation', models.CharField(max_length=50, null=True)),
                ('town_city', models.CharField(max_length=20, null=True)),
                ('post_code', models.CharField(max_length=10, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('product_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.Products')),
                ('principle_1', models.FloatField(default=0)),
                ('principle_2', models.FloatField(default=0)),
                ('principle_3', models.FloatField(default=0)),
                ('principle_4', models.FloatField(default=0)),
                ('principle_5', models.FloatField(default=0)),
                ('principle_6', models.FloatField(default=0)),
                ('principle_7', models.FloatField(default=0)),
                ('principle_8', models.FloatField(default=0)),
                ('principle_9', models.FloatField(default=0)),
                ('principle_10', models.FloatField(default=0)),
            ],
        ),
    ]
