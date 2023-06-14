from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from payment.models import Subscription
from servey_quiz_form.models import Form, Responses
from servey_quiz_form.serializers.resserializers import FormSerializer, ResponsesSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status
from django.db.models import Count
from rest_framework.response import Response
# class ResponseView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (JWTAuthentication,)
#     serializer_class = ResponsesSerializer

#     def get(self, request, code, response_code):
#         formInfo = Form.objects.filter(code=code).first()
#         if formInfo is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         elif not formInfo.allow_view_score and formInfo.creator != request.user.id:
#             return Response(status=status.HTTP_403_FORBIDDEN)

#         total_score = 0
#         score = 0

#         responseInfo = Responses.objects.filter(response_code=response_code).first()
#         if responseInfo is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
        
#         if formInfo.is_quiz:
#             for question in formInfo.questions.all():
#                 total_score += question.score
#                 for response in responseInfo.response.filter(answer_to__pk=question.pk):
#                     if response.answer_to.question_type == "short" or response.answer_to.question_type == "paragraph":
#                         if response.answer == response.answer_to.answer_key:
#                             score += response.answer_to.score
#                     elif response.answer_to.question_type == "multiple choice":
#                         answerKey = None
#                         for choice in response.answer_to.choices.all():
#                             if choice.is_answer:
#                                 answerKey = choice.id
#                         if answerKey is not None and str(answerKey) == str(response.answer):
#                             score += response.answer_to.score
#                     elif response.answer_to.question_type == "checkbox":
#                         # Get all responses for this question
#                         question_responses = responseInfo.response.filter(answer_to__pk=response.answer_to.pk)
#                         selected_answers = []
#                         correct_answers = []
#                         for question_response in question_responses:
#                             selected_answers.append(question_response.answer)
#                             for choice in question_response.answer_to.choices.all():
#                                 if choice.is_answer and choice.pk not in correct_answers:
#                                     correct_answers.append(choice.pk)

#                         # Calculate partial credit based on number of correct answers selected
#                         num_correct = len(set(selected_answers) & set(correct_answers))
#                         if len(correct_answers) > 0:
#                             partial_credit = response.answer_to.score * num_correct / len(correct_answers)
#                         else:
#                             partial_credit = 0
#                         score += partial_credit

#         serialized_form = FormSerializer(formInfo)
#         serialized_response = self.serializer_class(responseInfo, context={'request': request})

#         return Response({
#             "form": serialized_form.data,
#             "response": serialized_response.data,
#             "score": score,
#             "total_score": total_score
#         })


# class ResponseView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = ResponsesSerializer

#     def get(self, request, code, response_code):
#         form_info = Form.objects.filter(code=code).first()
#         if form_info is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         elif not form_info.allow_view_score:
#             return Response(status=status.HTTP_403_FORBIDDEN)

#         total_score = 0
#         score = 0

#         response_info = Responses.objects.filter(response_code=response_code).first()
#         if response_info is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         # Get the submission count based on the form's subscription plan
#         conduct_user = form_info.creator
#         subscription = Subscription.objects.filter(user=conduct_user).first()
#         if subscription is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         submission_counts = Responses.objects.filter(response_to=form_info, responder_email__isnull=False) \
#             .values('responder_email') \
#             .annotate(submission_count=Count('responder_email'))
        
#         # Get the submission count based on the form's subscription plan
#         plan_submission_counts = {
#             'A': 0,
#             'B': 0,
#             'C': 0,
#             'D': 0
#         }

#         for submission in submission_counts:
#             email = submission['responder_email']
#             count = submission['submission_count']
#             if email in plan_submission_counts:
#                 plan_submission_counts[email] = count

#         # Retrieve the submission count based on the form's subscription plan
#         form_plan = subscription.plan
#         submission_count = plan_submission_counts.get(form_plan, 0)

#         if form_info.is_quiz:
#             for question in form_info.questions.all():
#                 total_score += question.score
#                 for response in response_info.response.filter(answer_to__pk=question.pk):
#                     if response.answer_to.question_type == "short" or response.answer_to.question_type == "paragraph":
#                         if response.answer == response.answer_to.answer_key:
#                             score += response.answer_to.score
#                     elif response.answer_to.question_type == "multiple choice":
#                         answer_key = None
#                         for choice in response.answer_to.choices.all():
#                             if choice.is_answer:
#                                 answer_key = choice.id
#                         if answer_key is not None and str(answer_key) == str(response.answer):
#                             score += response.answer_to.score
#                     elif response.answer_to.question_type == "checkbox":
#                         # Get all responses for this question
#                         question_responses = response_info.response.filter(answer_to__pk=response.answer_to.pk)
#                         selected_answers = []
#                         correct_answers = []
#                         for question_response in question_responses:
#                             selected_answers.append(question_response.answer)
#                             for choice in question_response.answer_to.choices.all():
#                                 if choice.is_answer and choice.pk not in correct_answers:
#                                     correct_answers.append(choice.pk)

#                         # Calculate partial credit based on number of correct answers selected
#                         num_correct = len(set(selected_answers) & set(correct_answers))
#                         if len(correct_answers) > 0:
#                             partial_credit = response.answer_to.score * num_correct / len(correct_answers)
#                         else:
#                             partial_credit = 0
#                         score += partial_credit

#         serialized_form = FormSerializer(form_info)
#         serialized_response = self.serializer_class(response_info, context={'request': request})

#         response_data = {
#             "form": serialized_form.data,
#             "response": serialized_response.data,
#             "score": score,
#             "total_score": total_score,
#             "submission_count": submission_count
#         }

#         # Check if submission count exceeds the form's plan limit
#         form_limit = {
#             'A': 2,
#             'B': 6,
#             'C': 8,
#             'D': 9
#         }
#         if submission_count >= form_limit.get(form_plan, 0):
#             response_data["exceeded_limit"] = True
#         else:
#             response_data["exceeded_limit"] = False

#         return Response(response_data)



class ResponseView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ResponsesSerializer

    def get(self, request, code, response_code):
        form_info = Form.objects.filter(code=code).first()
        if form_info is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif not form_info.allow_view_score:
            return Response(status=status.HTTP_403_FORBIDDEN)

        total_score = 0
        score = 0

        response_info = Responses.objects.filter(response_code=response_code).first()
        if response_info is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        conduct_user = form_info.creator

        # Get the subscription plan of the conduct user
        subscription = Subscription.objects.filter(user=conduct_user).last()
        if subscription is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        form_plan = subscription.plan

        # Get the total number of submissions for the form
        submission_count = Responses.objects.filter(response_to=form_info, responder_email__isnull=False) \
            .values('responder_email') \
            .distinct() \
            .count()

        if form_info.is_quiz:
            # Calculate the score for the response
            for question in form_info.questions.all():
                total_score += question.score
                for response in response_info.response.filter(answer_to__pk=question.pk):
                    if response.answer_to.question_type == "short" or response.answer_to.question_type == "paragraph":
                        if response.answer == response.answer_to.answer_key:
                            score += response.answer_to.score
                    elif response.answer_to.question_type == "multiple choice":
                        answer_key = None
                        for choice in response.answer_to.choices.all():
                            if choice.is_answer:
                                answer_key = choice.id
                        if answer_key is not None and str(answer_key) == str(response.answer):
                            score += response.answer_to.score
                    elif response.answer_to.question_type == "checkbox":
                        # Get all responses for this question
                        question_responses = response_info.response.filter(answer_to__pk=response.answer_to.pk)
                        selected_answers = []
                        correct_answers = []
                        for question_response in question_responses:
                            selected_answers.append(question_response.answer)
                            for choice in question_response.answer_to.choices.all():
                                if choice.is_answer and choice.pk not in correct_answers:
                                    correct_answers.append(choice.pk)

                        # Calculate partial credit based on the number of correct answers selected
                        num_correct = len(set(selected_answers) & set(correct_answers))
                        if len(correct_answers) > 0:
                            partial_credit = response.answer_to.score * num_correct / len(correct_answers)
                        else:
                            partial_credit = 0
                        score += partial_credit

        serialized_form = FormSerializer(form_info)
        serialized_response = self.serializer_class(response_info, context={'request': request})

        response_data = {
            "form": serialized_form.data,
            "response": serialized_response.data,
            "score": score,
            "total_score": total_score,
            "submission_count": submission_count
        }

        # Check if the submission count exceeds the form's plan limit
        form_limit = {
            'A': 2,
            'B': 6,
            'C': 8,
            'D': 9
        }
        if submission_count >= form_limit.get(form_plan, 0):
            response_data["exceeded_limit"] = True
        else:
            response_data["exceeded_limit"] = False

        return Response(response_data)
# class ResponseView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (JWTAuthentication,)
#     serializer_class = ResponsesSerializer

#     def get(self, request, code, response_code):
#         formInfo = Form.objects.filter(code=code).first()
#         if formInfo is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         elif not formInfo.allow_view_score and formInfo.creator != request.user.id:
#             return Response(status=status.HTTP_403_FORBIDDEN)

#         total_score = 0
#         score = 0

#         responseInfo = Responses.objects.filter(response_code=response_code).first()
#         if responseInfo is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
        
#         if formInfo.is_quiz:
#             for question in formInfo.questions.all():
#                 total_score += question.score
#             _temp = []
#             for response in responseInfo.response.all():
#                 if response.answer_to.question_type == "short" or response.answer_to.question_type == "paragraph":
#                     if response.answer == response.answer_to.answer_key:
#                         score += response.answer_to.score
#                 elif response.answer_to.question_type == "multiple choice":
#                     answerKey = None
#                     for choice in response.answer_to.choices.all():
#                         if choice.is_answer:
#                             answerKey = choice.id
#                     if answerKey is not None and str(answerKey) == str(response.answer):
#                         score += response.answer_to.score
#                 elif response.answer_to.question_type == "checkbox" and response.answer_to.pk not in _temp:
#                     answers = []
#                     answer_keys = []
#                     for other_response in responseInfo.response.filter(answer_to__pk=response.answer_to.pk):
#                         answers.append(str(other_response.answer))
#                         for choice in other_response.answer_to.choices.all():
#                             if choice.is_answer and choice.pk not in answer_keys:
#                                 answer_keys.append(choice.pk)
#                         _temp.append(response.answer_to.pk)
#                     if set(answers) == set(answer_keys):
#                         score += response.answer_to.score
                        

#         serialized_form = FormSerializer(formInfo)
#         serialized_response = self.serializer_class(responseInfo, context={'request': request})

#         return Response({
#             "form": serialized_form.data,
#             "response": serialized_response.data,
#             "score": score,
#             "total_score": total_score
#         })

# class ResponseView(generics.RetrieveAPIView):
#     # Permission and authentication classes omitted for brevity
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (JWTAuthentication,)
#     serializer_class = ResponsesSerializer

#     def get(self, request, code, response_code):
#         form_info = Form.objects.filter(code=code).first()
#         if form_info is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         elif not form_info.allow_view_score and form_info.creator != request.user.id:
#             return Response(status=status.HTTP_403_FORBIDDEN)

#         total_score = 0
#         score = 0

#         response_info = Responses.objects.filter(response_code=response_code).first()
#         if response_info is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         if form_info.is_quiz:
#             # Check if there are any checkbox questions in the form
#             has_checkbox_questions = form_info.questions.filter(question_type='checkbox').exists()
#             if has_checkbox_questions:
#                 for question in response_info.questions.all():
#                     total_score += question.score
#                     if question.question_type == 'checkbox':
#                         # Group responses by their corresponding checkbox question
#                         checkbox_responses = {}
#                         for response in response_info.response.filter(answer_to=question):
#                             if response.answer in checkbox_responses:
#                                 checkbox_responses[response.answer].append(response)
#                             else:
#                                 checkbox_responses[response.answer] = [response]

#                         # Check if all answer keys have been selected for each group of responses
#                         for answer_key, responses in checkbox_responses.items():
#                             answer_keys = []
#                             for response in responses:
#                                 for choice in response.answer_to.choices.all():
#                                     if choice.is_answer and choice.pk not in answer_keys:
#                                         answer_keys.append(choice.pk)
#                             if sorted(answer_keys) == sorted(answer_key.split(',')):
#                                 score += question.score / len(checkbox_responses)
#             for question in form_info.questions.all():
#                 if question.question_type != 'checkbox':
#                     total_score += question.score / question.choices.count()

#                     for response in response_info.response.filter(answer_to=question):
#                         if question.question_type == "short" or question.question_type == "paragraph":
#                             if response.answer == response.answer_to.answer_key:
#                                 score += response.answer_to.score
#                         elif question.question_type == "multiple choice":
#                             answerKey = None
#                             for choice in response.answer_to.choices.all():
#                                 if choice.is_answer:
#                                     answerKey = choice.id
#                             if answerKey is not None and str(answerKey) == str(response.answer):
#                                 score += response.answer_to.score
#         else:
#             for question in form_info.questions.all():
#                 total_score += question.score / question.choices.count()

#                 for response in response_info.response.filter(answer_to=question):
#                     if question.question_type == "short" or question.question_type == "paragraph":
#                         if response.answer == response.answer_to.answer_key:
#                             score += response.answer_to.score
#                     elif question.question_type == "multiple choice":
#                         answerKey = None
#                         for choice in response.answer_to.choices.all():
#                             if choice.is_answer:
#                                 answerKey = choice.id
#                         if answerKey is not None and str(answerKey) == str(response.answer):
#                             score += response.answer_to.score

#         serialized_form = FormSerializer(form_info)
#         serialized_response = ResponsesSerializer(response_info, context={'request': request})

#         return Response({
#             "form": serialized_form.data,
#             "response": serialized_response.data,
#             "score": score,
#             "total_score": total_score
#         })


# class ResponseView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (JWTAuthentication,)
#     serializer_class = ResponsesSerializer

#     def get(self, request, code, response_code):
#         formInfo = Form.objects.filter(code=code).first()
#         if formInfo is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         elif not formInfo.allow_view_score and formInfo.creator != request.user.id:
#             return Response(status=status.HTTP_403_FORBIDDEN)

#         total_score = 0
#         score = 0

#         responseInfo = Responses.objects.filter(response_code=response_code).first()
#         if responseInfo is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
        
#         if formInfo.is_quiz:
#             for question in formInfo.questions.all():
            
#                 total_score += question.score
#             for response in responseInfo.response.all():
              
#                 if response.answer_to.question_type == "short" or response.answer_to.question_type == "paragraph":
#                     if response.answer == response.answer_to.answer_key:
#                         score += response.answer_to.score
#                 elif response.answer_to.question_type == "multiple choice":
#                     answerKey = None
#                     for choice in response.answer_to.choices.all():
#                         if choice.is_answer:
#                             answerKey = choice.id
#                     if answerKey is not None and str(answerKey) == str(response.answer):
#                         score += response.answer_to.score
#             _temp = []
#             for response in responseInfo.response.all():
#                 if response.answer_to.question_type == "checkbox" and response.answer_to.pk not in _temp:
#                     answers = []
#                     answer_keys = []
#                     for other_response in responseInfo.response.filter(answer_to__pk=response.answer_to.pk):
#                         answers.append(str(other_response.answer))
#                         for choice in other_response.answer_to.choices.all():
#                             if choice.is_answer and choice.pk not in answer_keys:
#                                 answer_keys.append(choice.pk)
#                         _temp.append(response.answer_to.pk)
#                     if answers == answer_keys:
#                         score += response.answer_to.score

#         serialized_form = FormSerializer(formInfo)
#         serialized_response = self.serializer_class(responseInfo, context={'request': request})

#         return Response({
#             "form": serialized_form.data,
#             "response": serialized_response.data,
#             "score": score,
#             "total_score": total_score
#         })
# class ResponseView(generics.RetrieveAPIView):
#     # Permission and authentication classes omitted for brevity
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (JWTAuthentication,)
#     serializer_class = ResponsesSerializer

#     def get(self, request, code, response_code):
#         form_info = Form.objects.filter(code=code).first()
#         if form_info is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         elif not form_info.allow_view_score and form_info.creator != request.user.id:
#             return Response(status=status.HTTP_403_FORBIDDEN)

#         total_score = 0
#         score = 0

#         response_info = Responses.objects.filter(response_code=response_code).first()
#         if response_info is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         if form_info.is_quiz:
#             for question in form_info.questions.all():
#                 total_score += question.score
#                 if question.question_type == 'checkbox':
#                     # Group responses by their corresponding checkbox question
#                     checkbox_responses = {}
#                     for response in response_info.response.filter(answer_to=question):
#                         if response.answer in checkbox_responses:
#                             checkbox_responses[response.answer].append(response)
#                         else:
#                             checkbox_responses[response.answer] = [response]

#                     # Check if all answer keys have been selected for each group of responses
#                     for answer_key, responses in checkbox_responses.items():
#                         answer_keys = []
#                         for response in responses:
#                             for choice in response.answer_to.choices.all():
#                                 if choice.is_answer and choice.pk not in answer_keys:
#                                     answer_keys.append(choice.pk)
#                         if sorted(answer_keys) == sorted(answer_key.split(',')):
#                             score += question.score / len(checkbox_responses)
#         serialized_form = FormSerializer(form_info)
#         serialized_response = ResponsesSerializer(response_info, context={'request': request})

#         return Response({
#             "form": serialized_form.data,
#             "response": serialized_response.data,
#             "score": score,
#             "total_score": total_score
#         })
