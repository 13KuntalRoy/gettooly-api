from rest_framework import serializers
from servey_quiz_form.models import Form, Questions, Choices, Responses, Answer
class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class ResponseSerializer(serializers.ModelSerializer):
    response = AnswerSerializer(many=True)

    class Meta:
        model = Responses
        fields = "__all__"

# class AnswerSerializer(serializers.ModelSerializer):
#     answer_to = serializers.PrimaryKeyRelatedField(queryset=Questions.objects.all())

#     class Meta:
#         model = Answer
#         fields = ('id', 'answer', 'answer_to')
# class ResponseSerializer(serializers.ModelSerializer):
#     response = AnswerSerializer(many=True, read_only=True)

#     class Meta:
#         model = Responses
#         fields = ('id', 'response_code', 'responder', 'responder_email', 'response', 'response_to')
# class ResponseSerializer(serializers.ModelSerializer):
#     response = AnswerSerializer(many=True, read_only=True)

#     class Meta:
#         model = Responses
#         fields = ('id', 'response_code', 'responder', 'responder_email', 'response', 'response_to')

#     def update(self, instance, validated_data):
#         response_data = validated_data.pop('response', None)

#         instance = super().update(instance, validated_data)

#         if response_data is not None:
#             answer_ids = [item.get('id', None) for item in response_data]
#             for answer in instance.response.all():
#                 if answer.id not in answer_ids:
#                     answer.delete()

#             for answer_data in response_data:
#                 answer_id = answer_data.get('id', None)
#                 if answer_id:
#                     answer_instance = Answer.objects.filter(id=answer_id, response=instance).first()
#                     if answer_instance:
#                         answer_serializer = AnswerSerializer(instance=answer_instance, data=answer_data, partial=True)
#                         answer_serializer.is_valid(raise_exception=True)
#                         answer_serializer.save()
#                 else:
#                     Answer.objects.create(response=instance, **answer_data)

#         return instance
