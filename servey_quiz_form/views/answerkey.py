

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import Questions,Form
from servey_quiz_form.serializers.answerkeyserializers import QuestionSerializer 
# class AnswerKeyView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (JWTAuthentication,)
#     def get_form(self, code):
#         try:
#             form = Form.objects.get(code=code)
#             return form
#         except Form.DoesNotExist:
#             raise Http404

#     def get_questions(self, form):
#         questions = form.questions.all()
#         return questions

#     def get(self, request, code):
#         form = self.get_form(code)
#         questions = self.get_questions(form)
#         serializer = QuestionSerializer(questions, many=True)
#         data = {
#             'form': {
#                 'title': form.title,
#                 'description': form.description,
#                 'is_quiz': form.is_quiz,
#             },
#             'questions': serializer.data,
#         }
#         return Response(data)

#     def post(self, request, code):
#         form = self.get_form(code)
#         if form.creator_id != request.user.id:
#             return Response({'message': 'You are not authorized to update this form.'}, status=status.HTTP_403_FORBIDDEN)

#         data = request.data
#         question_id = data.get('question_id')
#         answer_key = data.get('answer_key')

#         if not question_id or not answer_key:
#             return Response({'message': 'Question ID and answer key are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         question = get_object_or_404(Questions, pk=question_id)

#         if question.question_type == 'short' or question.question_type == 'paragraph':
#             question.answer_key = answer_key
#             question.save()
#         else:
#             for choice in question.choices.all():
#                 choice.is_answer = False
#                 choice.save()
#             if question.question_type == 'multiple choice':
#                 choice = question.choices.get(pk=answer_key)
#                 choice.is_answer = True
#                 choice.save()
#             else:
#                 choices = question.choices.filter(pk__in=[answer_key])
#                 for choice in choices:
#                     choice.is_answer = True
#                     choice.save()
#             question.save()

#         return Response({'message': 'Answer key updated successfully.'})
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from servey_quiz_form.models import Questions, Form
from servey_quiz_form.serializers.answerkeyserializers import QuestionSerializer 


class AnswerKeyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get_form(self, code):
        try:
            form = Form.objects.get(code=code)
            return form
        except Form.DoesNotExist:
            raise Http404

    def get_questions(self, form):
        questions = form.questions.all()
        return questions

    def get(self, request, code):
        form = self.get_form(code)
        questions = self.get_questions(form)
        serializer = QuestionSerializer(questions, many=True)
        data = {
            'form': {
                'title': form.title,
                'description': form.description,
                'is_quiz': form.is_quiz,
            },
            'questions': serializer.data,
        }
        return Response(data)

    def post(self, request, code):
        form = self.get_form(code)
        if form.creator_id != request.user.id:
            return Response({'message': 'You are not authorized to update this form.'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        question_id = data.get('question_id')
        answer_key = data.get('answer_key')

        if not question_id or answer_key is None:
            return Response({'message': 'Question ID and answer key are required.'}, status=status.HTTP_400_BAD_REQUEST)

        question = get_object_or_404(Questions, pk=question_id)

        if question.question_type == 'short' or question.question_type == 'paragraph':
            # update answer key for short/paragraph questions
            question.answer_key = answer_key
            question.save()
        elif question.question_type == 'multiple choice':
            # update answer key for multiple choice questions
            for choice in question.choices.all():
                if choice.pk == answer_key:
                    choice.is_answer = True
                else:
                    choice.is_answer = False
                choice.save()
            question.save()
        elif question.question_type == 'checkbox':
            # update answer key for checkbox questions
            if not isinstance(answer_key, list):
                return Response({'message': 'Answer key should be a list of choice ids.'}, status=status.HTTP_400_BAD_REQUEST)
            choices = question.choices.filter(pk__in=answer_key)
            # clear all previous answers
            question.choices.update(is_answer=False)
            for choice in choices:
                choice.is_answer = True
                choice.save()
            question.save()
        else:
            # invalid question type
            return Response({'message': 'Invalid question type.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Answer key updated successfully.'})