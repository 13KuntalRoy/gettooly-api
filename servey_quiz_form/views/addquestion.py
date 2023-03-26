from rest_framework import status

from rest_framework.generics import CreateAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import Choices, Questions,Form
from servey_quiz_form.serializers.answerkeyserializers import QuestionSerializer 

class CreateQuestionAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = QuestionSerializer

    def post(self, request, code):
        form_info = Form.objects.filter(code=code).first()

        if not form_info:
            return Response({'error': 'Form does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if form_info.creator_id != request.user.id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        choices = Choices.objects.create(choice='Option 1')
        question = Questions.objects.create(
            question_type='multiple choice', question='Untitled Question', required=False
        )
        question.choices.add(choices)
        form_info.questions.add(question)

        return Response({'question': QuestionSerializer(question).data, 'choices': {'id': choices.id, 'choice': choices.choice, 'is_answer': choices.is_answer}}, status=status.HTTP_201_CREATED)