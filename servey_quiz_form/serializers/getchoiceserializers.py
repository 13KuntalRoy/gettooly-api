from rest_framework import serializers
from servey_quiz_form.models import Choices,Questions

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = '__all__'

class GetChoicesSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Questions
        fields = '__all__'
        depth = 1

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Questions
        fields = '__all__'
        depth = 1