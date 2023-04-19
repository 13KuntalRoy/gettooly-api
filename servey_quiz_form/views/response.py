from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from servey_quiz_form.models import Form, Responses
from servey_quiz_form.serializers.resserializers import FormSerializer, ResponsesSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status
from rest_framework.response import Response


class ResponseView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = ResponsesSerializer

    def get(self, request, code, response_code):
        formInfo = Form.objects.filter(code=code).first()
        if formInfo is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif not formInfo.allow_view_score and formInfo.creator != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        total_score = 0
        score = 0

        responseInfo = Responses.objects.filter(response_code=response_code).first()
        if responseInfo is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        if formInfo.is_quiz:
            for question in formInfo.questions.all():
            
                total_score += question.score
            for response in responseInfo.response.all():
              
                if response.answer_to.question_type == "short" or response.answer_to.question_type == "paragraph":
                    if response.answer == response.answer_to.answer_key:
                        score += response.answer_to.score
                elif response.answer_to.question_type == "multiple choice":
                    answerKey = None
                    for choice in response.answer_to.choices.all():
                        if choice.is_answer:
                            answerKey = choice.id
                    if answerKey is not None and str(answerKey) == str(response.answer):
                        score += response.answer_to.score
            _temp = []
            for response in responseInfo.response.all():
                if response.answer_to.question_type == "checkbox" and response.answer_to.pk not in _temp:
                    answers = []
                    answer_keys = []
                    for other_response in responseInfo.response.filter(answer_to__pk=response.answer_to.pk):
                        answers.append(int(other_response.answer))
                        for choice in other_response.answer_to.choices.all():
                            if choice.is_answer and choice.pk not in answer_keys:
                                answer_keys.append(choice.pk)
                        _temp.append(response.answer_to.pk)
                    if answers == answer_keys:
                        score += response.answer_to.score

        serialized_form = FormSerializer(formInfo)
        serialized_response = self.serializer_class(responseInfo, context={'request': request})

        return Response({
            "form": serialized_form.data,
            "response": serialized_response.data,
            "score": score,
            "total_score": total_score
        })
