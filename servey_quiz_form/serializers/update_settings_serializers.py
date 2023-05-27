from rest_framework.serializers import ModelSerializer
from servey_quiz_form.models import Form
class edit_settings(ModelSerializer):
    class Meta:
        model = Form
        fields = ['collect_email','authenticated_responder','edit_after_submit','confirmation_message','is_quiz','allow_view_score','available_time','exam_duration','form_valid']