
from rest_framework import generics
from rest_framework import status


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import Choices, Form
from servey_quiz_form.serializers.createfromserializers import FormSerializer



class RemoveChoiceAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def delete(self, request, code):
        form = Form.objects.filter(code=code).first()

        if not form:
            return Response({"message": "Form does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if form.creator_id!= request.user.id:
            return Response({"message": "You do not have permission to edit this form"}, status=status.HTTP_403_FORBIDDEN)

        choice_id = request.data.get("id")
        choice = Choices.objects.filter(id=choice_id).first()

        if not choice:
            return Response({"message": "Choice does not exist"}, status=status.HTTP_404_NOT_FOUND)

        choice.delete()

        serializer = FormSerializer(form)

        return Response({"message": "Success", "form": serializer.data})