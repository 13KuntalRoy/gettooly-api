from rest_framework import serializers
from servey_quiz_form.models import Choices,Questions,Form
class ChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ('choice',)

class QuestionsSerializer(serializers.ModelSerializer):
    choices = ChoicesSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = ('question_type', 'question', 'required', 'choices')

class FormSerializer(serializers.ModelSerializer):
    questions = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = ('code', 'title', 'creator', 'questions')