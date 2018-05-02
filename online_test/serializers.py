from rest_framework import serializers, status
from .models import *
from online_test_frontend.models import *


class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = SingleChoiceCorrect
		fields = ('choice_1','choice_2','choice_3','choice_4')

class QuestionSerializer(serializers.ModelSerializer):
	singlechoicecorrect_question = ChoiceSerializer(many=True,required=False)

	class Meta:
		model = Question
		fields = ('content', 'figure','singlechoicecorrect_question')


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
