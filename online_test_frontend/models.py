from django.db import models
from datetime import datetime
from model_utils import Choices
from model_utils.fields import StatusField
from online_test.models import *

# Create your models here.

class Subscriptions(models.Model):
	student = models.ForeignKey(
		Student,
		on_delete=models.CASCADE,
		)
	exam = models.ForeignKey(
		Exam,
		on_delete=models.CASCADE,
		)
	
	event_status = Choices('Upcoming','Running','Halted','History')
	
	event = StatusField(choices_name='event_status')
	
	registered_on = models.DateTimeField(
		default = datetime.now,
		blank = True,
		)
	def __str__(self):
		return str(self.student.name)


class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ('album', 'order')
        ordering = ['order']

    def __unicode__(self):
        return '%d: %s' % (self.order, self.title)

# class Progress(models.Model):
# 	student = models.ForeignKey(Student,on_delete=models.CASCADE)
# 	start_time = 
