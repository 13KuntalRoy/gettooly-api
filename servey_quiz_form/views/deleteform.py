from rest_framework.generics import DestroyAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import  Form
from servey_quiz_form.serializers.createfromserializers import FormSerializer
class FormDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    queryset = Form.objects.all()
    serializer_class = FormSerializer
