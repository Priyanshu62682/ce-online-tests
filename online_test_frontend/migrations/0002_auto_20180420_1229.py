# Generated by Django 2.0.1 on 2018-04-20 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_test_frontend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriptions',
            old_name='joined_on',
            new_name='registered_on',
        ),
    ]
