# Generated by Django 2.0.5 on 2018-06-08 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_test', '0014_dynamic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dynamic',
            name='choice_1',
        ),
        migrations.RemoveField(
            model_name='dynamic',
            name='choice_2',
        ),
        migrations.RemoveField(
            model_name='dynamic',
            name='choice_3',
        ),
        migrations.RemoveField(
            model_name='dynamic',
            name='choice_4',
        ),
        migrations.AddField(
            model_name='dynamic',
            name='selected',
            field=models.CharField(default=False, max_length=1000),
        ),
        migrations.AlterField(
            model_name='dynamic',
            name='question_id',
            field=models.IntegerField(),
        ),
    ]
