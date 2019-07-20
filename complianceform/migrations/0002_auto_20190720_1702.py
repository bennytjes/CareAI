# Generated by Django 2.1.7 on 2019-07-20 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190720_1542'),
        ('complianceform', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Answers', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Entry_time', models.DateTimeField()),
                ('Product_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Products')),
                ('Version_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complianceform.Version')),
            ],
        ),
        migrations.AddField(
            model_name='answers',
            name='Entry_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complianceform.Entry'),
        ),
        migrations.AddField(
            model_name='answers',
            name='Question_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complianceform.Questions'),
        ),
    ]
