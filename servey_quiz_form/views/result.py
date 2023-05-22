from accounts.models import ConductUser
from servey_quiz_form.serializers.resultserializers import ResultSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
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