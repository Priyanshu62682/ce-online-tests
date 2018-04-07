# Generated by Django 2.0.1 on 2018-02-13 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_test', '0007_auto_20180213_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='online_test.Section'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exam',
            name='test_id',
            field=models.CharField(default='W3AwQ5', max_length=50, unique=True, verbose_name='test id'),
        ),
    ]
