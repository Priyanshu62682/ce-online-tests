# Generated by Django 2.0.1 on 2018-04-22 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_test', '0008_remove_exam_test_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='online_test.Exam'),
        ),
        migrations.AlterField(
            model_name='question',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='online_test.Section'),
        ),
        migrations.AlterField(
            model_name='section',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='online_test.Exam'),
        ),
    ]