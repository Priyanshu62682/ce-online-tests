# Generated by Django 2.0.1 on 2018-04-11 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_test', '0015_auto_20180411_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='test_id',
            field=models.CharField(default='UuoDMbVh6Kpe', max_length=50, unique=True, verbose_name='test id'),
        ),
    ]
