from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import Choices, Questions,Form
from servey_quiz_form.serializers.answerkeyserializers import QuestionSerializer
from servey_quiz_form.serializers.deletequestionserializers import DeleteQuestionSerializer 

class DeleteQuestionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = DeleteQuestionSerializer
    
    def delete(self, request, code, question):
        form = get_object_or_404(Form, code=code)
        if form.creator_id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        question = get_object_or_404(Questions, id=question)
        for choice in question.choices.all():
            choice.delete()
        question.delete()
        return Response({"message": "Success"})