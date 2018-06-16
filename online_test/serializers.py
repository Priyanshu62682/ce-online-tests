from rest_framework import serializers, status
from .models import *
from online_test_frontend.models import *
import json

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
	class Meta:
		model = Question
		fields = ('id','serial','content', 'figure','question_choices_question')


class SectionSerializer(serializers.ModelSerializer):
	question_section = QuestionSerializer(many=True,required=False)

	class Meta:
		model = Section
		fields = ('section_type','section_instructions','question_section')


class PartSerializer(serializers.ModelSerializer):
	section_part = SectionSerializer(many=True,required=False)

	class Meta:
		model = Part
		fields = ('name','section_part')



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

class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Dynamic
		fields = ('choice_1','choice_2','choice_3','choice_4')