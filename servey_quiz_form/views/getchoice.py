
from django.shortcuts import get_object_or_404
from rest_framework.generics import (

    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from  servey_quiz_form.models import Questions, Form
from servey_quiz_form.serializers.getchoiceserializers import GetChoicesSerializer


class Get_choice(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = GetChoicesSerializer

    def get_queryset(self):
        form = get_object_or_404(Form, code=self.kwargs.get('code'))
        if form.creator_id != self.request.user.id:
            self.permission_denied(
                self.request, message="You don't have permission to access this form.")
        question = get_object_or_404(Questions, id=self.kwargs.get('question'))
        queryset = [question]  # wrap the question in a list
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)