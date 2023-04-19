from rest_framework import serializers
from servey_quiz_form.models import Form, Questions, Answer, Choices

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ['id', 'choice']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_to', 'answer']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = ['id', 'question', 'question_type', 'choices']

class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = ['id', 'title', 'description', 'code', 'creator', 'questions']