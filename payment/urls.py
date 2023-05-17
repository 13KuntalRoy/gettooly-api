from django.urls import path
from payment.views import (
    CancelSubscriptionView, HandlePaymentView, SubscriptionList, SubscriptionDetail, create_subscription, 
    CreateOneMonthSubscriptionView, PaymentIntentView
)

urlpatterns = [
    path('subscriptions/', SubscriptionList.as_view(), name='subscription-list'),
    path('subscriptions/<str:pk>/', SubscriptionDetail.as_view(), name='subscription-detail'),
    path('subscriptions/create/', create_subscription, name='create-subscription'),
    path('cancel-subscription/<str:subscription_id>/', CancelSubscriptionView.as_view(), name='cancel-subscription'),
    path('subscriptions/create-one-month/', CreateOneMonthSubscriptionView.as_view(), name='create-one-month-subscription'),
    path('payment-intent/', PaymentIntentView.as_view(), name='payment-intent'),
    path('payment-handel/', HandlePaymentView.as_view(), name='payment-handel')
]