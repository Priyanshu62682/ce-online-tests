from django.db import models
from django.utils.crypto import get_random_string
import hashlib
from datetime import datetime  
from model_utils import Choices
from model_utils.fields import StatusField
from django.urls import reverse_lazy,reverse
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

	test_id = models.CharField(
		unique=True,
		max_length=50,
		blank=False,
		verbose_name = "test id",
		default = generate_rand_id(),
		)
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

	draft = models.BooleanField(
		default = True,
		help_text = "Uncheck to launch the test",
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

	def save(self, *args, **kwargs):
		self.test_id = get_random_string
		if not self.url:
			self.url = self.generate_url()

		super(Exam, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse_lazy('online_test:dashboard')

	def __str__(self):
		return self.title

# class Part(models.Model):
# 	exam = models.ForeignKey(Exam,on_delete = models.CASCADE)

# 	name = models.CharField(
# 		unique = True,
# 		max_length=50,
# 		blank=False,
# 		verbose_name = "part name",
# 		)
# 	def part_total_questions(self):
# 		questions = self.question_set.count()
# 		return questions

# 	def part_calculate_marks(self):
# 		marks = self.question_set.count()*self.positive_marks
# 		return marks

# 	def __str__(self):
# 		return self.name

class Section(models.Model):
	STATUS = Choices('single_choice_correct_type','multiple_choice_correct_type','integer_answer_type')
	
	part_choices = Choices('Physics','Chemistry','Maths')
	
	exam = models.ForeignKey(Exam,on_delete = models.CASCADE)

	part = StatusField(choices_name='part_choices')

	# selects question type from status variable defined above
	section_type = StatusField()

	positive_marks = models.IntegerField(
		help_text = "Example: +4",
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
	def section_calculate_marks(self):
		marks = self.question_set.count()*self.positive_marks
		return marks

	def section_total_questions(self):
		questions = self.question_set.count()
		return questions

	def __str__(self):
		return str(self.section_type)

class Question(models.Model):
	exam = models.ForeignKey(Exam,on_delete = models.CASCADE)

	part_choices = Choices('Physics','Chemistry','Maths')
	
	part = StatusField(choices_name='part_choices')

	section = models.ForeignKey(Section,on_delete = models.CASCADE)

	content = models.CharField(
		max_length=1000,
		blank = False,
		help_text = "Enter the question",
		)

	figure = models.ImageField(upload_to='diagrams/',
		blank = True,
		)

	def get_choices(self):
		marks = self.singlechoicecorrect_set.select_related('question_id')
		return marks

	def __str__(self):
		return str(self.id)

class SingleChoiceCorrect(models.Model):

	STATUS = Choices('Choice-1','Choice-2','Choice-3','Choice-4')

	question_id = models.ForeignKey(Question,on_delete=models.CASCADE)
	
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
	correct_choice = StatusField()


	def __str__(self):
		return str(self.question_id)