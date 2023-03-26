from rest_framework.serializers import ModelSerializer
from servey_quiz_form.models import Form
class edit_description(ModelSerializer):
    class Meta:
        model = Form
        fields = ['description']