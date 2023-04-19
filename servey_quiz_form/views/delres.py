from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from servey_quiz_form.models import Form, Responses
from servey_quiz_form.serializers.delresserializers import DeleteResponsesSerializer
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied

class DeleteResponses(generics.DestroyAPIView):
    serializer_class = DeleteResponsesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        code = self.kwargs.get('code')
        form = Form.objects.filter(code=code).first()
        if not form:
            raise Http404('Form does not exist')
        print(form.creator)
        print(self.request.user.id)
        if form.creator.id != self.request.user.id:
            
            raise PermissionDenied('You are not authorized to delete responses for this form')
        return form

    def destroy(self, request, *args, **kwargs):
        form = self.get_object()
        responses = Responses.objects.filter(response_to=form)
        for response in responses:
            for i in response.response.all():
                i.delete()
            response.delete()
        return Response({'message': 'Responses have been deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
