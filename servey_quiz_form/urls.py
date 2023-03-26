from django.urls import include, path
from servey_quiz_form.views.addquestion import CreateQuestionAPIView
from servey_quiz_form.views.answerkey import AnswerKeyView

from servey_quiz_form.views.createfrom import CreateForm
from servey_quiz_form.views.deletechoice import RemoveChoiceAPIView
from servey_quiz_form.views.deletequestion import DeleteQuestionView
from servey_quiz_form.views.editresponseview import DeleteResponseAPIView, FormResponseEditAPIView
from servey_quiz_form.views.formview import FormView
from servey_quiz_form.views.responsesview import ResponseViewSet, ResponsesAPI
from servey_quiz_form.views.score import EditScoreView
from servey_quiz_form.views.updatetitle import UpdateTitle
from servey_quiz_form.views.updatedescription import UpdateDescription
from servey_quiz_form.views.update_background_color import Update_background_color
from servey_quiz_form.views.update_text_color import Update_text_color
from servey_quiz_form.views.update_settings import Update_settings
from servey_quiz_form.views.editquestion import EditQuestionAPIView
from servey_quiz_form.views.addchoice import AddChoiceAPIView
from servey_quiz_form.views.updatechoice import EditChoiceAPIView
from servey_quiz_form.views.getchoice import Get_choice
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'response', ResponseViewSet, basename='response')

urlpatterns = [
   
    path("form/create",CreateForm.as_view(), name="create_form"),
    path('form/<str:code>/', FormView.as_view(), name='form-detail'),
    path("form/update/title/<str:code>/",UpdateTitle.as_view(), name="update_title"),
    path("form/update/description/<str:code>/",UpdateDescription.as_view(), name="update_description"),
    path("form/update/background_color/<str:code>/",Update_background_color.as_view(), name="update_background_color"),
    path("form/update/text_color/<str:code>/",Update_text_color.as_view(), name="update_text_color"),
    path("form/update/setting/<str:code>/",Update_settings.as_view(), name="update_setting"),
    path('form/<str:code>/create_question', CreateQuestionAPIView.as_view(), name='create_question'),
    path('forms/<str:code>/questions/<int:question>/', DeleteQuestionView.as_view(), name='delete_question'),
    path('form/edit_question/<str:code>/', EditQuestionAPIView.as_view(), name='edit_question'),
    path('form/<str:code>/add-choice/', AddChoiceAPIView.as_view(), name='add_choice'),
    path('form/<str:code>/choices/<int:choice_id>/', EditChoiceAPIView.as_view(), name='edit_choice'),
    path('form/<str:code>/get_choice/<str:question>',Get_choice.as_view(), name="get_choice"),
    path('form/<str:code>/remove-choice/', RemoveChoiceAPIView.as_view(), name='remove-choice'),
    path('forms/<str:code>/answer-key/', AnswerKeyView.as_view(), name='answer_key'),
    path('edit_score/<str:code>/', EditScoreView.as_view(), name='edit_score'),
    path('responses/<pk>/' , ResponsesAPI.as_view()),
    path('form/<str:code>/response/<str:response_code>/edit/', FormResponseEditAPIView.as_view(), name='form-response-edit'),
    path('form/<str:code>/responses/delete', DeleteResponseAPIView.as_view(), name='delete_responses'),
    path('' , include(router.urls)),








]