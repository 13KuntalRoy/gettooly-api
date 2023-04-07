from django.urls import path
from payment.views import (
    HandlePaymentView, SubscriptionList, SubscriptionDetail, create_subscription, cancel_subscription,
    CreateOneMonthSubscriptionView, PaymentIntentView
)

urlpatterns = [
    path('subscriptions/', SubscriptionList.as_view(), name='subscription-list'),
    path('subscriptions/<int:pk>/', SubscriptionDetail.as_view(), name='subscription-detail'),
    path('subscriptions/create/', create_subscription, name='create-subscription'),
    path('subscriptions/<int:subscription_id>/cancel/', cancel_subscription, name='cancel-subscription'),
    path('subscriptions/create-one-month/', CreateOneMonthSubscriptionView.as_view(), name='create-one-month-subscription'),
    path('payment-intent/', PaymentIntentView.as_view(), name='payment-intent'),
    path('payment-handel/', HandlePaymentView.as_view(), name='payment-handel')
]