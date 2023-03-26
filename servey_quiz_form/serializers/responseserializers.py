from rest_framework import serializers
from servey_quiz_form.models import Responses
class ResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responses
        exclude = ['created_at' , 'updated_at']