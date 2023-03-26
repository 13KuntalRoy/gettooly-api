

from servey_quiz_form.models import Answer,Responses

from rest_framework import serializers

class FormResponseEditRequestSerializer(serializers.Serializer):
    email_address = serializers.EmailField(required=False)
    responses = serializers.DictField(child=serializers.ListField(), required=True)

    def validate(self, data):
        responses = data['responses']
        form = self.context['form']
        for question_id, answers in responses.items():
            question = form.questions.filter(id=question_id).first()
            if question is None:
                raise serializers.ValidationError(f"Question with id '{question_id}' does not exist in the form.")
            if question.required and not answers:
                raise serializers.ValidationError(f"Question with id '{question_id}' is required.")
            if not isinstance(answers, list):
                raise serializers.ValidationError(f"Answers for question with id '{question_id}' should be a list.")
            if question.question_type == 'mcq' and len(answers) > 1:
                raise serializers.ValidationError(f"Multiple answers provided for question with id '{question_id}', "
                                                  f"but only one answer allowed.")
            for answer in answers:
                if question.question_type == 'mcq':
                    if not question.choices.filter(choice=answer).exists():
                        raise serializers.ValidationError(f"'{answer}' is not a valid choice for question "
                                                          f"with id '{question_id}'.")
                if question.question_type == 'short_answer':
                    if len(answer) > 5000:
                        raise serializers.ValidationError(f"Short answer for question with id '{question_id}' "
                                                          f"should not exceed 5000 characters.")
                if question.question_type == 'long_answer':
                    if len(answer) > 10000:
                        raise serializers.ValidationError(f"Long answer for question with id '{question_id}' "
                                                          f"should not exceed 10000 characters.")
        return data


class DeleteResponseSerializer(serializers.Serializer):
    confirmation = serializers.CharField(required=True)

    def validate_confirmation(self, value):
        if value != 'delete':
            raise serializers.ValidationError('Invalid confirmation')
        return value
    

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer', 'answer_to')

class ResponseSerializer(serializers.ModelSerializer):
    response = AnswerSerializer(many=True)

    class Meta:
        model = Responses
        fields = ('id','responder_ip', 'responder', 'responder_email', 'response')