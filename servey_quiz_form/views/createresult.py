from rest_framework import generics, status
from rest_framework.response import Response

from servey_quiz_form.models import Result
from servey_quiz_form.serializers.resultserializers import ResultSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ResultListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)