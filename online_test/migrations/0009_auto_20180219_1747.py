# Generated by Django 2.0.1 on 2018-02-19 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_test', '0008_auto_20180213_1806'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='status_type',
            new_name='section_type',
        ),
        migrations.AlterField(
            model_name='exam',
            name='test_id',
            field=models.CharField(default='3U7YxA', max_length=50, unique=True, verbose_name='test id'),
        ),
    ]