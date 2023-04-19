from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from servey_quiz_form.models import Form
from servey_quiz_form.serializers.responsesserializers import FormSerializer, QuestionSerializer, AnswerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
class Responses(APIView):
    permission_classes = [
        IsAuthenticated,
     ]
    authentication_classes = (JWTAuthentication,)
    def get(self, request, code):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        form = Form.objects.filter(code=code).first()
        if not form:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if form.creator != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        form_serializer = FormSerializer(form)
        questions = form.questions.all()
        responses_summary = []
        choice_answered = {}
        filtered_responses_summary = {}
        for question in questions:
            answers = question.answers.all()
            question_serializer = QuestionSerializer(question)
            if question.question_type in ["multiple choice", "checkbox"]:
                choice_answered[question.question] = {}
                for answer in answers:
                    choice = answer.answer_to.choices.get(id=answer.answer).choice
                    choice_answered[question.question][choice] = choice_answered.get(question.question, {}).get(choice, 0) + 1
            answers_serializer = AnswerSerializer(answers, many=True)
            responses_summary.append({"question": question_serializer.data, "answers": answers_serializer.data})
        for answer in choice_answered:
            filtered_responses_summary[answer] = {}
            keys = choice_answered[answer].values()
            for choice in choice_answered[answer]:
                filtered_responses_summary[answer][choice] = choice_answered[answer][choice]
        return Response({
            "form": form_serializer.data,
            "responses": form.responses.values(),
            "responses_summary": responses_summary,
            "filtered_responses_summary": filtered_responses_summary
        })