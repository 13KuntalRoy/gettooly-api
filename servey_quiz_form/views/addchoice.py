from rest_framework import status

from rest_framework import status

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from  servey_quiz_form.models import Questions, Form,Choices

from  servey_quiz_form.serializers.choiceserializers import ChoicesSerializer

class AddChoiceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    def post(self, request, code):
        if not request.user.is_authenticated:
            return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        formInfo = Form.objects.filter(code=code)
        # Checking if form exists
        if formInfo.count() == 0:
            return Response({"message": "Form does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            formInfo = formInfo[0]
        # Checking if form creator is user
        if formInfo.creator_id != request.user.id:
            return Response({"message": "You do not have permission to edit this form"}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        question_id = data.get("question")
        question = Questions.objects.get(pk=question_id)
        choice = Choices(choice="Option")
        choice.save()
        question.choices.add(choice)
        return Response({"message": "Success", "choice": ChoicesSerializer(choice).data}, status=status.HTTP_201_CREATED)