from rest_framework.serializers import ModelSerializer
from servey_quiz_form.models import Choices,Questions
class ChoicesSerializer(ModelSerializer):
    class Meta:
        model = Choices
        fields = ['id', 'choice', 'is_answer']
class edit_choices(ModelSerializer):
    class Meta:
        model = Questions
        fields = ['choices']

