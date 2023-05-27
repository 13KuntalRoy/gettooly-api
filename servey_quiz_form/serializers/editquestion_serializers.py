from django.forms import ValidationError
from rest_framework import serializers
from servey_quiz_form.models import Form,Choices,Questions,Answer
from django.core.exceptions import ObjectDoesNotExist

class ChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ['id', 'choice', 'is_answer']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer', 'answer_to']


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
                  'is_quiz', 'allow_view_score', 'createdAt', 'updatedAt', 'questions']


class UpdateQuestionChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    choice = serializers.CharField(max_length=5000)
    is_answer = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.choice = validated_data.get('choice', instance.choice)
        instance.is_answer = validated_data.get('is_answer', instance.is_answer)
        instance.save()
        return instance


class UpdateQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    question = serializers.CharField(max_length=100000)
    question_type = serializers.CharField(max_length=20)
    required = serializers.BooleanField()
    score = serializers.IntegerField(required=False)
    answer_key = serializers.CharField(max_length=5000, required=False)
    choices = UpdateQuestionChoiceSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.required = validated_data.get('required', instance.required)
        instance.score = validated_data.get('score', instance.score)
        instance.answer_key = validated_data.get('answer_key', instance.answer_key)
        instance.save()

        choices_data = validated_data.get('choices')
        if choices_data:
            for choice_data in choices_data:
                choice_id = choice_data.pop('id')
                try:
                    choice = instance.choices.get(id=choice_id)
                    choice_serializer = UpdateQuestionChoiceSerializer(choice, data=choice_data)
                    choice_serializer.is_valid(raise_exception=True)
                    choice_serializer.save()
                except ObjectDoesNotExist:
                    raise ValidationError(f"Choice with id {choice_id} not found")

        return instance