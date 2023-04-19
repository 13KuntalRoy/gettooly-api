from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from servey_quiz_form.models import Form
from servey_quiz_form.serializers.getformserializers import FormSerializer

class UserFormListView(APIView):
    def get(self, request, user_id):
        try:
            forms = Form.objects.filter(creator=user_id)
        except Form.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)
