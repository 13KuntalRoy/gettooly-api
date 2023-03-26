
from rest_framework.exceptions import NotFound
from rest_framework import generics, permissions,status

from rest_framework import status

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from  servey_quiz_form.models import Questions, Form
from servey_quiz_form.serializers.createfromserializers import FormSerializer

from  servey_quiz_form.serializers.editquestion_serializers import UpdateQuestionSerializer, UpdateQuestionChoiceSerializer,FormSerializer


class EditQuestionAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = (JWTAuthentication,)

    def get_form(self, code):
        try:
            form = Form.objects.get(code=code)
            if form.creator_id != self.request.user.id:
                raise permissions.PermissionDenied()
            return form
        except Form.DoesNotExist:
            raise generics.NotFound()

    def get_question(self, form, question_id):
        try:
            question = form.questions.get(id=question_id)
            return question
        except Questions.DoesNotExist:
            raise NotFound(f"Question with id {question_id} not found in form with code {form.code}")

    def patch(self, request, code, *args, **kwargs):
        form = self.get_form(code)
        data = request.data
        question_id = data.get('id')
        question_data = data.get('question_data')

        if question_data is None or question_id is None:
            return Response({'error': 'question_data and id fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        question = self.get_question(form, question_id)

        serializer = UpdateQuestionSerializer(question, data=question_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        choices_data = data.get('choices_data')
        if choices_data:
            choices_serializer = UpdateQuestionChoiceSerializer(data=choices_data, many=True)
            choices_serializer.is_valid(raise_exception=True)
            for choice_data in choices_serializer.validated_data:
                choice_id = choice_data.pop('id')
                question.choices.filter(id=choice_id).update(**choice_data)

        updated_form = Form.objects.get(id=form.id)
        serializer = FormSerializer(updated_form)
        return Response(serializer.data)