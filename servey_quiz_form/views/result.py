from django.http import Http404
from accounts.models import ConductUser, UserQuiz
from servey_quiz_form.models import Form, Result
from servey_quiz_form.serializers.resultserializers import ResultSerializer, Show_result

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
class FormResultsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = ResultSerializer

    def get_queryset(self):
        # Retrieve the conduct user based on the user's authentication or any other criteria
        conduct_user = ConductUser.objects.get(id=self.request.user.id)
        
        # Retrieve the form ID from the URL parameters or request data
        form_id = self.kwargs['form_id']
        
        # Retrieve the form associated with the conduct user
        form = conduct_user.creator.get(id=form_id)

        # Retrieve the results associated with the form
        return form.result_to.all()


class UserQuizResultListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = ResultSerializer
    

    def get_queryset(self):
        # Retrieve the UserQuiz instance based on the provided userquiz_id
        userquiz_id = self.kwargs['userquiz_id']
        userquiz = UserQuiz.objects.get(id=userquiz_id)
        
        # Retrieve the associated quiz results for the UserQuiz instance
        results = Result.objects.filter(responder=userquiz,show_score=True)
        
        return results
# class ResultListAPIView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (JWTAuthentication,)
#     queryset = Result.objects.all()
#     serializer_class = Show_result

#     def perform_create(self, serializer):
#         show_score = self.request.data.get('show_score')
#         print("+++++++++++++++++++++++++++++++++++++")
#         print(show_score)
#         if show_score:
#             # Update show_score for all Result instances
#             Result.objects.update(show_score=show_score)

#         serializer.save()
# class ResultListAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (JWTAuthentication,)
#     queryset = Result.objects.all()
#     serializer_class = Show_result

#     def perform_update(self, serializer):
#         show_score = self.request.data.get('show_score')
#         if show_score:
#             # Update show_score for all Result instances
#             Result.objects.update(show_score=show_score)

#         serializer.save()
class ResultListAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    queryset = Result.objects.all()
    serializer_class = Show_result

    def perform_update(self, serializer):
        show_score = self.request.data.get('show_score')
        form_id = self.kwargs['form_id']
        conduct_user = ConductUser.objects.get(id=self.request.user.id)
        
        form = conduct_user.creator.get(id=form_id)

        if show_score is not None:
            if show_score:  # If show_score is True
                form.result_to.filter(show_score=False).update(show_score=True)
            else:  # If show_score is False
                form.result_to.filter(show_score=True).update(show_score=False)

        serializer.save()
