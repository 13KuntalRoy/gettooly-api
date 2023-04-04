from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from payment.models import Subscription
from payment.serializers import SubscriptionSerializer, PaymentIntentSerializer
import stripe
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payment.models import Subscription
from payment.serializers import SubscriptionSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class SubscriptionList(ListAPIView):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user)
class SubscriptionDetail(RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

@api_view(["POST"])
def create_subscription(request):
    serializer = PaymentIntentSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    subscription = serializer.save()
    serializer = SubscriptionSerializer(subscription)
    return Response(serializer.data)

@api_view(["POST"])
def cancel_subscription(request, subscription_id):
    # Get the subscription object for the logged in user
    user = request.user
    try:
        subscription = Subscription.objects.get(id=subscription_id, user=user)
    except Subscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Cancel the subscription in Stripe
    stripe.api_key = user.stripe_secret_key
    stripe.Subscription.delete(subscription.stripe_subscription_id)

    # Update the subscription status in the database
    subscription.status = "canceled"
    subscription.save()

    serializer = SubscriptionSerializer(subscription)
    return Response(serializer.data)
class CreateOneMonthSubscriptionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentIntentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the customer object for the logged in user
        user = request.user
        customer = stripe.Customer.objects.get(user=user.stripe_customer_id)

        # Create a new subscription for the customer
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{
                "plan": serializer.validated_data["plan"]
            }],
            default_payment_method=serializer.validated_data["payment_method_id"],
            expand=["latest_invoice.payment_intent"],
            trial_period_days=30, # set the subscription to last for one month
        )

        # Create a new payment intent for the subscription
        payment_intent = stripe.PaymentIntent.create(
            payment_method=serializer.validated_data["payment_method_id"],
            customer=customer.id,
            amount=serializer.validated_data["amount"],
            currency="usd",
            payment_method_types=[serializer.validated_data["payment_method_type"]],
            subscription=subscription.id,
            confirm=True,
        )

        # Update the subscription status based on the payment intent status
        if payment_intent.status == "succeeded":
            subscription.status = "active"
            subscription.save()
        else:
            subscription.status = "incomplete"
            subscription.save()

        serializer = SubscriptionSerializer(subscription)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentIntentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentIntentSerializer
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = PaymentIntentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        data = {
            'message': 'Subscription created successfully!',
            'subscription_id': subscription.stripe_subscription_id
        }
        return Response(data, status=201)