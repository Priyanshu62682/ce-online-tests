from rest_framework import serializers, status
from .models import *
from online_test_frontend.models import *
import json
from django.core.exceptions import ObjectDoesNotExist

class QuestionChoicesSerializer(serializers.ModelSerializer):
	#choices_modified = serializers.CharField(source='modified_choices',read_only=True)  
	choices = serializers.SerializerMethodField('clean_json')        
	class Meta:
		model = QuestionChoices
		fields = ('choices',)

	def clean_json(self, obj):
		return obj.choices

	# def to_representation(self, instance):
	# 	data = super(QuestionChoicesSerializer, self).to_representation(instance)
	# 	result_data={"status" : 200,"message" : "Category List"}
	# 	result_data["response"]=data
	# 	return result_data

	# def __init__(self, *args, **kwargs):
	# 	fields = kwargs.pop('fields', None)
	# 	print(fields)
	# 	super(QuestionChoicesSerializer,self).__init__(*args, **kwargs)

	# 	context = kwargs.get('context', None)
	# 	if fields:
			
	# 		print(fields)
	# 	else:
	# 		print("In else")


class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = SingleChoiceCorrect
		fields = ('choice_1','choice_2','choice_3','choice_4')

class QuestionSerializer(serializers.ModelSerializer):
	#singlechoicecorrect_question = ChoiceSerializer(many=True,required=False)
	question_choices_question = QuestionChoicesSerializer(many=True,required=False)
	previous_data = serializers.SerializerMethodField()

	def get_previous_data(self, obj):
		exam = self.context.get("exam").first()
		student = self.context.get("student")
		#print(obj.serial)
		try:
			pastbackup = Dynamic.objects.get(test_id=exam,student_id=student)
			try:
				previous_choice = pastbackup.progress[str(obj.serial)]
				print(previous_choice[0])
				previous_choice = int(previous_choice[0])
			except:
				previous_choice = None

			try:
				previous_flag = pastbackup.progress_flags[str(obj.serial)]
				previous_flag = int(previous_flag[0])
			except:
				previous_flag = None

			previous_data ={
					'previous_choice':previous_choice,
					'previous_flag':previous_flag
				} 


		except ObjectDoesNotExist:
			previous_data = None
		
		return previous_data

	class Meta:
		model = Question
		fields = ('id','serial','content', 'figure','question_choices_question','previous_data')


class SectionSerializer(serializers.ModelSerializer):
	question_section = QuestionSerializer(many=True,required=False)

	class Meta:
		model = Section
		fields = ('section_type','section_instructions','question_section')


class PartSerializer(serializers.ModelSerializer):
	section_part = SectionSerializer(many=True,required=False)
	total_questions = serializers.SerializerMethodField()
	first_serial = serializers.SerializerMethodField()

	def get_total_questions(self,obj):
		exam = self.context.get("exam").first()
		total_questions = Question.objects.filter(exam=exam, part=obj).count()
		return total_questions

	def get_first_serial(self, obj):
		exam = self.context.get("exam").first()
		try:
			serial = Question.objects.filter(exam=exam, part=obj).order_by('serial').first().serial
		except:
			serial = None
		return serial

	class Meta:
		model = Part
		fields = ('name','total_questions','first_serial','section_part')




class ExamSerializer(serializers.ModelSerializer):

	part_exam = PartSerializer(many=True,required=False)

	class Meta:
		model = Exam
		fields = ('id', 'title', 'description', 'instructions', 'part_exam')



#Test
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('order', 'title', 'duration')

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks')
