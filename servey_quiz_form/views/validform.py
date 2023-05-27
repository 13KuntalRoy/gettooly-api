from rest_framework import generics
from django.utils import timezone

from servey_quiz_form.serializers.resultserializers import FormSerializer
from servey_quiz_form.models import Form
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication


class ValidFormsAPIView(generics.UpdateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = (JWTAuthentication,)
    serializer_class = FormSerializer

    def get_queryset(self):
        # Retrieve the form based on the form_id URL parameter
        form_id = self.kwargs['form_id']
        return Form.objects.filter(id=form_id)

    def perform_update(self, serializer):
        form = serializer.instance

        # Check if the available time is over the current time
        if form.available_time and form.available_time < timezone.now():
            form.form_valid = False
            form.save()
