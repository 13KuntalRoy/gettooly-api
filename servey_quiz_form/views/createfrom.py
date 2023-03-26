
import random
import string
from rest_framework import status
from accounts.models import ConductUser
from rest_framework import status
from rest_framework.generics import (

    CreateAPIView
)
from servey_quiz_form.serializers.createfromserializers import FormSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import Choices, Questions,Form

from servey_quiz_form.serializers import *
class CreateForm(CreateAPIView):
    permission_classes = [
        IsAuthenticated,
     ]
    authentication_classes = (JWTAuthentication,)
    serializer_class = FormSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        title = data.get("title")

        if not title:
            return Response({"message": "Title required"}, status=status.HTTP_400_BAD_REQUEST)

        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))

        choices = Choices(choice="Option 1")
        choices.save()

        question = Questions(question_type="multiple choice", question="Untitled Question", required=False)
        question.save()
        question.choices.add(choices)
        question.save()

        form = Form(code=code, title=title, creator=ConductUser.objects.get(id=self.request.user.id))
        form.save()
        form.questions.add(question)
        form.save()

        serializer = FormSerializer(form)

        return Response(serializer.data, status=status.HTTP_201_CREATED)