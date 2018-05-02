# Generated by Django 2.0.1 on 2018-05-01 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_test', '0011_auto_20180501_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='part_exam', to='online_test.Exam'),
        ),
        migrations.AlterField(
            model_name='part',
            name='name',
            field=models.CharField(max_length=50, verbose_name='part name'),
        ),
        migrations.AlterField(
            model_name='question',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_part', to='online_test.Part'),
        ),
        migrations.AlterField(
            model_name='question',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_section', to='online_test.Section'),
        ),
        migrations.AlterField(
            model_name='section',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_exam', to='online_test.Exam'),
        ),
        migrations.AlterField(
            model_name='section',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_part', to='online_test.Part'),
        ),
    ]
