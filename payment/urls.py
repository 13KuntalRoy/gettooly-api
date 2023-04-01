from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from payment import views

urlpatterns = [
    path('subscriptions/', views.SubscriptionList.as_view()),
    path('subscriptions/<int:pk>/', views.SubscriptionDetail.as_view()),
    path('payment_intents/', views.PaymentIntentView.as_view()),
    path('subscriptions/one-month/', views.CreateOneMonthSubscriptionView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)