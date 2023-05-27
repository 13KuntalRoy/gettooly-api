from rest_framework import serializers
from servey_quiz_form.models import Result, Form
class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
class Show_result(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = ['show_score']
