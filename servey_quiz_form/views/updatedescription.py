
from rest_framework.generics import (

    UpdateAPIView
)

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import Form

from servey_quiz_form.serializers.update_description_serializers import edit_description
class UpdateDescription(UpdateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = (JWTAuthentication,)

    queryset = Form.objects.all()
    serializer_class = edit_description
    lookup_field = 'code'

    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = edit_description(instance=instance, many=False)
        return Response(serializer.data)