# Generated by Django 2.0.1 on 2018-04-20 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_test', '0005_auto_20180420_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='test_id',
            field=models.CharField(default='CiRFTqctrOtc', max_length=50, unique=True, verbose_name='test id'),
        ),
    ]