from rest_framework import serializers
from servey_quiz_form.models import Form, Questions, Choices, Answer, Responses


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ['id', 'choice', 'is_answer']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = ['id', 'question', 'question_type', 'choices', 'answer_key', 'score']


class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        fields = '__all__'
    


class ResponsesSerializer(serializers.ModelSerializer):
    response = AnswerSerializer(many=True)

    class Meta:
        model = Responses
        fields = "__all__"


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = ['id', 'title', 'description', 'questions', 'is_quiz', 'allow_view_score', 'creator', 'code']