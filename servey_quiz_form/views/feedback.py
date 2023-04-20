from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from servey_quiz_form.models import Form
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    authentication_classes = (JWTAuthentication,)

    def post(self, request, code):
        form_info = Form.objects.filter(code=code).first()
        # Checking if form exists
        if not form_info:
            return Response({'error': 'Form not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Checking if form creator is user
        if form_info.creator.id != request.user.id:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        if not form_info.is_quiz:
            return Response({'error': 'Invalid operation.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            question = form_info.questions.filter(id=data["question_id"]).first()
            if not question:
                return Response({'error': 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)
            question.feedback = data["feedback"]
            question.save()
            return Response({'message': "Success"})
