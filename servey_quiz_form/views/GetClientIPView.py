from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from servey_quiz_form.serializers.IPResponseSerializer import IPResponseSerializer

class GetClientIPView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    serializer_class = IPResponseSerializer

    def get(self, request, format=None):
        ip = self.get_client_ip(request)
        serializer = self.serializer_class({'ip': ip})
        return Response(serializer.data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
