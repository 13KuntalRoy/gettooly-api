from rest_framework import status

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import  Form

from servey_quiz_form.serializers import *
from servey_quiz_form.serializers.editquestion_serializers import QuestionsSerializer


class EditScoreView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    def get_form_info(self, code):
        form_info = Form.objects.filter(code=code)
        if form_info.count() == 0:
            return None
        return form_info[0]

    def get_question(self, form_info, question_id):
        question = form_info.questions.filter(id=question_id)
        if question.count() == 0:
            return None
        return question[0]

    def post(self, request, code):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        form_info = self.get_form_info(code)
        if form_info is None:
            return Response({'detail': 'Form not found.'}, status=status.HTTP_404_NOT_FOUND)

        if form_info.creator_id != request.user.id:
            return Response({'detail': 'You are not the creator of this form.'}, status=status.HTTP_403_FORBIDDEN)

        if not form_info.is_quiz:
            return Response({'detail': 'This is not a quiz form.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        question_id = data.get('question_id')
        score = data.get('score', 0)

        question = self.get_question(form_info, question_id)
        if question is None:
            return Response({'detail': 'Question not found.'}, status=status.HTTP_400_BAD_REQUEST)

        question.score = score
        question.save()

        serializer = QuestionsSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)