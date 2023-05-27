from rest_framework import serializers
from servey_quiz_form.models import Choices,Questions,Form


class ChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ['id', 'choice', 'is_answer']

class QuestionsSerializer(serializers.ModelSerializer):
    choices = ChoicesSerializer(many=True)

    class Meta:
        model = Questions
        fields = ['id', 'question', 'question_type', 'required', 'answer_key', 'score', 'feedback', 'choices']

class FormSerializer(serializers.ModelSerializer):
    questions = QuestionsSerializer(many=True)

    class Meta:
        model = Form
        fields = ['id', 'code', 'title', 'description', 'creator', 'background_color', 'text_color',
                  'collect_email', 'authenticated_responder', 'edit_after_submit', 'confirmation_message',
                  'is_quiz', 'allow_view_score', 'createdAt', 'updatedAt', 'questions','form_valid','available_time','exam_duration']