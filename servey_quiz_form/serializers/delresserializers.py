from rest_framework import serializers

from servey_quiz_form.models import Form, Questions, Choices, Answer, Responses


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('id', 'title', 'description', 'code', 'is_quiz', 'authenticated_responder', 'collect_email', 'allow_view_score', 'creator', 'questions')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer', 'answer_to')

class ResponsesSerializer(serializers.ModelSerializer):
    response = AnswerSerializer(many=True)

    class Meta:
        model = Responses
        fields = ('id', 'response_code', 'responder', 'responder_email', 'response')

class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.StringRelatedField(many=True)

    class Meta:
        model = Questions
        fields = ('id', 'question', 'question_type', 'score', 'answer_key', 'choices')

class FormQuestionSerializer(serializers.ModelSerializer):
    choices = serializers.StringRelatedField(many=True)

    class Meta:
        model = Questions
        fields = ('id', 'question', 'question_type', 'score', 'answer_key', 'choices')

class FormResponsesSerializer(serializers.ModelSerializer):
    response = AnswerSerializer(many=True)
    questions = FormQuestionSerializer(many=True)

    class Meta:
        model = Responses
        fields = ('id', 'response_code', 'responder', 'responder_email', 'response', 'questions')

class DeleteResponsesSerializer(serializers.Serializer):
    success = serializers.CharField(max_length=200)