
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions,status

from rest_framework import status
from rest_framework import generics

from rest_framework.response import Response


from servey_quiz_form.models import  Form, Responses

from servey_quiz_form.serializers.editresponseserializers import DeleteResponseSerializer, FormResponseEditRequestSerializer
class FormResponseEditAPIView(generics.GenericAPIView):
    serializer_class = FormResponseEditRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
            code = self.kwargs.get('code')
            response_code = self.kwargs.get('response_code')
            form = get_object_or_404(Form, code=code)
            response = get_object_or_404(form.responses.all(), response_code=response_code, responder=self.request.user)
            return response

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['form'] = self.get_object().response_to
        return context

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FormResponseEditRequestSerializer
        return self.serializer_class

    def put(self, request, *args, **kwargs):
        response = self.get_object()
        serializer = self.get_serializer(response, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteResponseAPIView(generics.DestroyAPIView):
    serializer_class = DeleteResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        code = self.kwargs['code']
        queryset = Responses.objects.filter(response_to__code=code)
        return queryset

    def perform_destroy(self, instance):
        instance.response.all().delete()
        instance.delete()
        return Response({'message': 'Success'})