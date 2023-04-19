from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from servey_quiz_form.models import Form, Responses, Answer
from servey_quiz_form.serializers.editresponseserializers import ResponseSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

from rest_framework.generics import RetrieveUpdateAPIView



class edit_response(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ResponseSerializer

    def get_object(self):
        code = self.kwargs.get('code')
        response_code = self.kwargs.get('response_code')
        form_info = self.get_form_info(code)
        response = self.get_response(response_code, form_info)
        return response

    def get_form_info(self, code):
        try:
            return Form.objects.get(code=code)
        except Form.DoesNotExist:
            raise Http404

    def get_response(self, response_code, form_info):
        try:
            return Responses.objects.get(response_code=response_code, response_to=form_info)
        except Responses.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        response = self.get_object()
        form_info = response.response_to

        if form_info.authenticated_responder:
            if not request.user.is_authenticated:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            if response.responder != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

        if form_info.authenticated_responder and not response.responder:
            response.responder = request.user
            response.save()

        if form_info.collect_email:
            response.responder_email = request.data.get("email-address")
            response.save()

        # Deleting all existing answers
        response.response.all().delete()

        # Saving new answers
        for question_id, answers in request.data.items():
            if question_id == "csrfmiddlewaretoken" or question_id == "email-address":
                continue

            question = form_info.questions.get(id=question_id)
            for answer_text in answers:
                answer = Answer(answer=answer_text, answer_to=question)
                answer.save()
                response.response.add(answer)

        serializer = self.get_serializer(response)
        return Response(serializer.data)
# @api_view(['GET', 'PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def edit_response(request, code, response_code):
#     form = get_object_or_404(Form, code=code)
#     response = get_object_or_404(Responses, response_code=response_code, response_to=form)

#     if request.method == 'GET':
#         serializer = ResponseSerializer(response)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = ResponseSerializer(response, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
