
from rest_framework.generics import (

    UpdateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import Form

from servey_quiz_form.serializers.update_settings_serializers import edit_settings
class Update_settings(UpdateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = (JWTAuthentication,)

    queryset = Form.objects.all()
    serializer_class = edit_settings
    lookup_field = 'code'

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        updated_instance = self.get_object()
        updated_serializer = edit_settings(updated_instance, many=False)
        return Response(updated_serializer.data)