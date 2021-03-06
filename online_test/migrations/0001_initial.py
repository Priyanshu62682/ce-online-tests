# Generated by Django 2.0.1 on 2018-06-09 09:09

import datetime
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dynamic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', jsonfield.fields.JSONField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the test title', max_length=100, unique=True, verbose_name='test name')),
                ('url', models.SlugField(blank=True, help_text='Enter the url for the test', max_length=100)),
                ('description', models.CharField(blank=True, help_text='Test description', max_length=300, verbose_name='test description')),
                ('instructions', models.CharField(blank=True, help_text='Test instructions', max_length=500, verbose_name='instructions')),
                ('created_on', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('test_type', model_utils.fields.StatusField(choices=[('Free', 'Free'), ('Mock', 'Mock'), ('Paid', 'Paid')], default='Free', max_length=100, no_check_for_status=True)),
                ('published', models.BooleanField(default=False, help_text='Check to launch the test')),
            ],
            options={
                'verbose_name': 'test',
            },
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='part name')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='part_exam', to='online_test.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(help_text='Enter the question', max_length=1000)),
                ('figure', models.ImageField(blank=True, upload_to='diagrams/')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.Exam')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_part', to='online_test.Part')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_json', jsonfield.fields.JSONField()),
                ('test_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', model_utils.fields.StatusField(choices=[('single_choice_correct_type', 'single_choice_correct_type'), ('multiple_choice_correct_type', 'multiple_choice_correct_type'), ('integer_answer_type', 'integer_answer_type')], default='single_choice_correct_type', max_length=100, no_check_for_status=True)),
                ('positive_marks', models.IntegerField(help_text='Example: +4')),
                ('negative_marks', models.IntegerField(help_text='Example: -1')),
                ('section_instructions', models.CharField(blank=True, help_text='Enter instructions for the section', max_length=1000)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_exam', to='online_test.Exam')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_part', to='online_test.Part')),
            ],
        ),
        migrations.CreateModel(
            name='SingleChoiceCorrect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_1', models.CharField(max_length=50, verbose_name='Choice 1')),
                ('choice_2', models.CharField(max_length=50, verbose_name='Choice 2')),
                ('choice_3', models.CharField(max_length=50, verbose_name='Choice 3')),
                ('choice_4', models.CharField(max_length=50, verbose_name='Choice 4')),
                ('correct_choice', model_utils.fields.StatusField(choices=[('Choice-1', 'Choice-1'), ('Choice-2', 'Choice-2'), ('Choice-3', 'Choice-3'), ('Choice-4', 'Choice-4')], default='Choice-1', max_length=100, no_check_for_status=True)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='singlechoicecorrect_question', to='online_test.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_username', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(help_text='Full Name', max_length=50)),
                ('batch', model_utils.fields.StatusField(choices=[('11-Studying', '11-Studying'), ('12-Studying', '12-Studying'), ('12-Pass', '12-Pass'), ('other', 'other')], default='11-Studying', max_length=100, no_check_for_status=True)),
                ('Address', models.CharField(blank=True, max_length=200)),
                ('joined_on', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='student_username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.Student'),
        ),
        migrations.AddField(
            model_name='result',
            name='test_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='online_test.Exam'),
        ),
        migrations.AddField(
            model_name='question',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_section', to='online_test.Section'),
        ),
        migrations.AddField(
            model_name='dynamic',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.Student'),
        ),
        migrations.AddField(
            model_name='dynamic',
            name='test_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='online_test.Exam'),
        ),
    ]
