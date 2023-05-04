
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import UserQuiz
from servey_quiz_form.models import Form, Questions , Responses , Answer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from servey_quiz_form.serializers.responseserializers import ResponsesSerializer

from servey_quiz_form.utils import generate_random_string
from rest_framework import viewsets
from rest_framework.decorators import action

class ResponseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    queryset = Responses.objects.all()
    serializer_class = ResponsesSerializer

    # @action(detail=False, methods=['post'])
    # def store_responses(self, request):
    #     try:
    #         data = request.data

    #         if data.get('form_id') is None or data.get('responses') is None:
    #                 return Response(
    #                     {
    #                     'status' : False ,
    #                     'message' : 'form_id and responses both are required',
    #                     'data' : {}})

    #         responses = data.get('responses')
    #         response_obj = Responses.objects.create(
    #             response_code = generate_random_string(15),
    #             response_to = Form.objects.get(id = data.get('form_id')),
    #             responder_ip=data.get('responder_ip'),
    #             responder_email=data.get('responder_email'),
    #             responder=UserQuiz.objects.get(id=self.request.user.id)
    #         )


    #         for response in responses:
    #             print(response)
    #             question_obj = Questions.objects.get(id = response['question'])
    #             if question_obj.question_type == 'checkbox':
    #                 for answer in response['answer']:
    #                     answer_obj = Answer.objects.create(
    #                             answer = answer,
    #                             answer_to = question_obj
    #                     )
    #                 response_obj.response.add(answer_obj)

    #             else:
    #                 answer_obj = Answer.objects.create(
    #                             answer = response['answer'],
    #                             answer_to = question_obj
    #                     )
                    
    #                 response_obj.response.add(answer_obj)

    #         return Response({'status' : True ,'message' : 'response captured' , 'data' : {"response_code" :response_obj.response_code}})

    #     except Exception as e:
    #         print(e)
    #         return Response({'status' : False ,'message' : 'something went wrong' , 'data' : {}})
    @action(detail=False, methods=['post'])
    def store_responses(self, request):
        try:
            data = request.data

            if data.get('form_id') is None or data.get('responses') is None:
                    return Response(
                        {
                        'status' : False ,
                        'message' : 'form_id and responses both are required',
                        'data' : {}})

            responses = data.get('responses')
            response_obj = Responses.objects.create(
                response_code = generate_random_string(15),
                response_to = Form.objects.get(id = data.get('form_id')),
                responder_ip=data.get('responder_ip'),
                responder_email=data.get('responder_email'),
                responder=UserQuiz.objects.get(id=self.request.user.id)
            )


            for response in responses:
                print(response)
                question_obj = Questions.objects.get(id = response['question'])
                if question_obj.question_type == 'checkbox':
                    for answer in response['answer']:
                        answer_obj = Answer.objects.create(
                                answer = answer,
                                answer_to = question_obj
                        )
                        response_obj.response.add(answer_obj)
                else:
                    answer_obj = Answer.objects.create(
                                answer = response['answer'],
                                answer_to = question_obj
                        )
                    
                    response_obj.response.add(answer_obj)

            return Response({'status' : True ,'message' : 'response captured' , 'data' : {"response_code" :response_obj.response_code}})

        except Exception as e:
            print(e)
            return Response({'status' : False ,'message' : 'something went wrong' , 'data' : {}})

# class ResponsesAPI(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (JWTAuthentication,)
#     def get(self , request , pk):
#         try:
#             print(request.user)
#             formInfo = Form.objects.get(code = pk)
#             self.check_object_permissions(request , formInfo)
#             responsesSummary = []
#             choiceAnswered = { }
#             non_choices_answer = {}

#             for question in formInfo.questions.all():
#                 print("AAAAAAAAAAAAAAAAAA")
#                 answers = Answer.objects.filter(answer_to = question.id)

#                 if question.question_type == "multiple choice" or question.question_type == "checkbox":
#                     choiceAnswered[question.question] = choiceAnswered.get(question.question ,{})


#                     for choice in question.choices.all():
#                         print("BBBBBBBBBBBBBBBBB")
#                         choiceAnswered[question.question][choice.choice] = 0 


#                     print(answers)
#                     for answer in answers:
#                         print("CCCCCCCCCCCCCCCCCCCC")
#                         choice = answer.answer_to.choices.get(choice = answer.answer).choice
#                         choiceAnswered[question.question][choice] = choiceAnswered.get(question.question , {}).get(choice ,0) + 1
#                         print(choiceAnswered)
#                     print("bokachoda")



#                 else:
#                     print("DDDDDDDDDDDDD")
#                     for answer in answers:
#                         print("EE")
#                         if non_choices_answer.get(question.question):
#                             non_choices_answer[question.question].append(answer.answer)
#                         else:
#                             non_choices_answer[question.question] = [answer.answer] 
#                 print("RESSSSSSSSSSSSSSS")
    
#                 responsesSummary.append({'question' :question , 'answer' : answer})


            
#             final_list = []
#             print("FFFFFFFFFFFFFFFFFFFFFUUUUCK")

#             for answer in choiceAnswered:
#                 print("FFFFFFF")
#                 final_dict = {}
#                 final_dict['question'] = answer
#                 final_dict['answer'] = choiceAnswered[answer]

#                 final_dict['chartData'] = {
#                     'labels' : choiceAnswered[answer].keys(),
#                     'datasets' : [
#                         {'data' : choiceAnswered[answer].values()}
#                     ]
#                 }

#                 final_dict['keys'] = choiceAnswered[answer].keys()
#                 final_dict['values'] = choiceAnswered[answer].values()

#                 final_list.append(final_dict)
#                 print(final_list)


#             return Response({
#                 'status' : True,
#                 'message' : 'success',
#                 'data' : {'count' : Responses.objects.filter(response_to__code = pk).count(),'data' : final_list , 'non_choices_answer' : non_choices_answer}
#             })

#         except Exception as e:
#             print(e)
#             return Response({
#                 'status': False,
#                 'message' : 'something went wrong or you dont have permission to view this',
#                 'data' : {}
#             })
class ResponsesAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get(self, request, pk):
        try:
            form_info = Form.objects.get(code=pk)
            self.check_object_permissions(request, form_info)
            responses_summary = []
            choice_answered = {}
            non_choices_answer = {}

            for question in form_info.questions.all():
                answers = Answer.objects.filter(answer_to=question.id)

                if question.question_type in ["multiple choice", "checkbox"]:
                    choice_answered[question.question] = {}

                    for choice in question.choices.all():
                        choice_answered[question.question][choice.choice] = 0

                    for answer in answers:
                        choices = answer.answer if isinstance(answer.answer, list) else [answer.answer]
                        for choice in choices:
                            choice_answered[question.question][choice] = choice_answered[question.question].get(choice, 0) + 1

                else:
                    for answer in answers:
                        if non_choices_answer.get(question.question):
                            non_choices_answer[question.question].append(answer.answer)
                        else:
                            non_choices_answer[question.question] = [answer.answer]

                responses_summary.append({'question': question, 'answer': answer})

            final_list = []

            for answer in choice_answered:
                final_dict = {}
                final_dict['question'] = answer
                final_dict['answer'] = choice_answered[answer]

                final_dict['chartData'] = {
                    'labels': choice_answered[answer].keys(),
                    'datasets': [
                        {'data': choice_answered[answer].values()}
                    ]
                }

                final_dict['keys'] = choice_answered[answer].keys()
                final_dict['values'] = choice_answered[answer].values()

                final_list.append(final_dict)

            return Response({
                'status': True,
                'message': 'success',
                'data': {
                    'count': Responses.objects.filter(response_to__code=pk).count(),
                    'data': final_list,
                    'non_choices_answer': non_choices_answer
                }
            })

        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message': 'something went wrong or you dont have permission to view this',
                'data': {}
            })
