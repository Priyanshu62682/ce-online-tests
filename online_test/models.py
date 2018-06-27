from django.db import models
from django.utils.crypto import get_random_string
import hashlib
from datetime import datetime  
from model_utils import Choices
from model_utils.fields import StatusField
from django.urls import reverse_lazy,reverse
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import JSONField
from jsonfield import JSONField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



class Exam(models.Model):

	# to generate the unique random id for test_id
	def generate_rand_id():
		randstr = ""
		return get_random_string()
		while True:
			randstr = get_random_string(length=6)
			if Exam.object.filter(test_id=randstr).count() is 0:
				break
		return randstr

	# test_id = models.CharField(
	# 	unique=True,
	# 	max_length=50,
	# 	blank=False,
	# 	verbose_name = "test id",
	# 	default = generate_rand_id(),
	# 	)
	title = models.CharField(
		unique=True,
		max_length=100,
		blank=False,
		help_text = "Enter the test title",
		verbose_name = "test name",
		)
	url = models.SlugField(
		max_length = 100,
		blank=True,
		help_text = "Enter the url for the test",
		)
	description = models.CharField(
		max_length=300,
		verbose_name = "test description",
		help_text = "Test description",
		blank = True,
		)
	instructions = models.CharField(
		max_length=500,
		verbose_name = "instructions",
		help_text = "Test instructions",
		blank = True,
		)
	created_on = models.DateTimeField(
		default = datetime.now,
		blank = True,
		)
	test_choices = Choices('Free','Mock','Paid')
	test_type = StatusField(choices_name='test_choices')
	published = models.BooleanField(
		default = False,
		help_text = "Check to launch the test",
		)
	test_completed = models.BooleanField(
		default = False,
		)
	class Meta:
		verbose_name = ("test")

	# function to generate the md5 hash value (not in use currently)
	def generate_test_id(self):
		s = str(self.pk)+'ce'
		m = hashlib.md5()
		m.update(s.encode('utf-8'))
		return str(m.hexdigest())

	# function to generate the unique url - currently set to be same as title
	def generate_url(self):
		url = self.title.replace(" ","")
		s = self.title.replace(" ","")
		m = hashlib.md5()
		m.update(s.encode('utf-8'))
		print(str(m.hexdigest()))
		return url

	def related_parts(self):
		parts = Part.objects.filter(exam=self)
		return parts

	def save(self, *args, **kwargs):
		self.test_id = get_random_string
		if not self.url:
			self.url = self.generate_url()

		super(Exam, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse_lazy('online_test:dashboard')

	def __str__(self):
		return self.title

class Part(models.Model):
	exam = models.ForeignKey(Exam,related_name='part_exam',on_delete = models.CASCADE)

	name = models.CharField(
		unique = False,
		max_length=50,
		blank=False,
		verbose_name = "part name",
		)
	# def part_total_questions(self):
	# 	questions = self.question_set.count()
	# 	return questions

	# def part_calculate_marks(self):
	# 	marks = self.question_set.count()*self.positive_marks
	# 	return marks

	def __str__(self):
		return self.name

class Section(models.Model):
	STATUS = Choices('single_choice_correct_type','multiple_choice_correct_type','integer_type','match_type')
	
	# part_choices = Choices('Physics','Chemistry','Maths')
	# part = StatusField(choices_name='part_choices')
	exam = models.ForeignKey(Exam, related_name='section_exam', on_delete = models.CASCADE)
	
	part = models.ForeignKey(Part,related_name='section_part',on_delete=models.CASCADE)

	# selects question type from status variable defined above
	section_type = StatusField()
	positive_marks = models.IntegerField(
		help_text = "Example: +4",
		blank = False,
		)
	per_option_positive_marks = models.IntegerField(
		help_text = "Example: +1",
		blank = False,
		)
	negative_marks = models.IntegerField(
		help_text = "Example: -1",
		blank = False,
		)
	section_instructions = models.CharField(
		max_length = 1000,
		blank = True,
		help_text = "Enter instructions for the section",
		)
	# def section_calculate_marks(self):
	# 	marks = self.question_set.count()*self.positive_marks
	# 	return marks

	# def section_total_questions(self):
	# 	questions = self.question_set.count()
	# 	return questions

	def __str__(self):
		return str(self.section_type)

class Question(models.Model):
	exam = models.ForeignKey(Exam,on_delete = models.CASCADE)
	# part_choices = Choices('Physics','Chemistry','Maths')
	# part = StatusField(choices_name='part_choices')
	part = models.ForeignKey(Part,related_name='question_part',on_delete=models.CASCADE)
	section = models.ForeignKey(Section,related_name='question_section',on_delete = models.CASCADE)
	content = models.CharField(
		max_length=1000,
		blank = False,
		help_text = "Enter the question",
		)
	figure = models.ImageField(upload_to='diagrams/',
		blank = True,
		)
	serial = models.IntegerField(
		blank = False,
		)
	def get_choices(self):
		choices_instance = QuestionChoices.objects.get(question_id=self)
		choices_json = choices_instance.choices
		return choices_json

	def correct_choice(self):
		choices_instance = QuestionChoices.objects.get(question_id=self)

		
		correct_choice = choices_instance.correct_choice
		
		return correct_choice

	def __str__(self):
		return str(self.content)


class SingleChoiceCorrect(models.Model):

	CHOICES = (
		('A','choice_1'),
		('B','choice_2'),
		('C','choice_3'),
		('D','choice_4'))
	question_id = models.ForeignKey(Question,related_name='singlechoicecorrect_question',on_delete=models.CASCADE)
	choice_1 = models.CharField(
		max_length=50,
		blank=False,
		verbose_name = "Choice 1",
		)
	choice_2 = models.CharField(
		max_length=50,
		blank=False,
		verbose_name = "Choice 2",
		)
	choice_3 = models.CharField(
		max_length=50,
		blank=False,
		verbose_name = "Choice 3",
		)
	choice_4 = models.CharField(
		max_length=50,
		blank=False,
		verbose_name = "Choice 4",
		)
	correct_choice = models.CharField(max_length=10, choices=CHOICES)
	
	def __str__(self):
		return str(self.question_id)

class QuestionChoices(models.Model):

	question_id = models.ForeignKey(Question,related_name='question_choices_question',on_delete=models.CASCADE)
	section = models.ForeignKey(Section,on_delete=models.CASCADE)
	choices = JSONField()
	correct_choice = JSONField()
	
	def __str__(self):
		return str(self.question_id)

class Student(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	birth_date = models.DateField(null=True, blank=True)
	student_username = models.CharField(
		unique=True,
		blank=False,
		max_length=20,
		)
	name = models.CharField(
		blank=False,
		max_length=50,
		
		)	
	class_status = Choices('11-Studying','12-Studying','12-Pass','other')
	batch = StatusField(choices_name='class_status')
	#to be detailed
	Address = models.CharField(
		max_length=200,
		blank=True,
		)
	joined_on = models.DateTimeField(
		default = datetime.now,
		blank = True,
		)
	def __str__(self):
		return str(self.student_username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)





class Result(models.Model):
	test_id = models.ForeignKey(Exam,on_delete=models.PROTECT)
	student_username = models.ForeignKey(Student,on_delete=models.CASCADE)
	#add hex code to be in the url instead of username
	result_json = JSONField()
	test_completed = models.BooleanField(
		default = False,
		blank = False,
		)
	def __str__(self):
		return str(self.student_username)

class Dynamic(models.Model):
	student_id= models.ForeignKey(Student,on_delete=models.CASCADE)
	test_id=models.ForeignKey(Exam,on_delete=models.PROTECT)
	progress=JSONField(blank=True)

	def __str__(self):
		return str(self.student_id)

