
from django.core.exceptions import PermissionDenied

from rest_framework import status

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import Choices, Form

from servey_quiz_form.serializers.choiceserializers import ChoicesSerializer
class EditChoiceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    def get_object(self, code, choice_id):
        try:
            form = Form.objects.get(code=code)
 
            choice = Choices.objects.get(id=choice_id)
            # if choice not in form.questions.choices.all():
            #     raise Choices.DoesNotExist
            if form.creator_id != self.request.user.id:
                raise PermissionDenied
            return choice
        except (Form.DoesNotExist, Choices.DoesNotExist, PermissionDenied):
            return None
    
    def patch(self, request, code, choice_id):
        choice = self.get_object(code, choice_id)
        if not choice:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChoicesSerializer(instance=choice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)