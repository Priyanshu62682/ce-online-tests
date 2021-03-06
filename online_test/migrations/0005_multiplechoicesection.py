# Generated by Django 2.0.5 on 2018-06-12 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_test', '0004_section_section_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleChoiceSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive_marks', models.IntegerField(help_text='Example: +4')),
                ('positive_marks_per_question', models.IntegerField(help_text='Example: +1')),
                ('negative_marks', models.IntegerField(help_text='Example: -1')),
                ('section_instructions', models.CharField(blank=True, help_text='Enter instructions for the section', max_length=1000)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multiplesection_exam', to='online_test.Exam')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multiplesection_part', to='online_test.Part')),
            ],
        ),
    ]
