from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from servey_quiz_form.models import Form
from servey_quiz_form.serializers.getformserializers import FormSerializer


class FormView(APIView):
    def get(self, request, code):
        form = get_object_or_404(Form, code=code)
        serializer = FormSerializer(form)
        return Response(serializer.data)