from rest_framework import serializers
from servey_quiz_form.models import Form, Responses, Answer, Questions


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id', 'question']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer']


class ResponseSerializer(serializers.ModelSerializer):
    response_to = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())
    response = AnswerSerializer(many=True)

    class Meta:
        model = Responses
        fields = [ 'response_to', 'responder_ip', 'responder_email', 'response']


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Form
        fields = ['code', 'title', 'background_color', 'text_color', 'confirmation_message', 'edit_after_submit', 'is_quiz', 'allow_view_score', 'collect_email', 'authenticated_responder', 'questions']