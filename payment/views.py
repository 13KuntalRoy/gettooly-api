from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import ConductUser
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
from django.utils import timezone
from datetime import datetime, timedelta
stripe.api_key = "sk_test_51LKc43SJstE3ZNVN1qUjmXNFy1ieonJnEQV4r8JZcZIhBu9IU8K7CweoKSEmwvuPOumeeWdgQxI06cWYq1YDGlj700YkcQHgd9"
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

# class PaymentIntentView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (JWTAuthentication,)

#     def post(self, request):
#         request_data = request.data
#         serializer = PaymentIntentSerializer(data=request_data)
#         serializer.is_valid(raise_exception=True)

#         validated_data = serializer.validated_data
#         amount = validated_data["amount"]
#         plan = validated_data["plan"]
#         duration = validated_data["duration"]
#         payment_method_id = validated_data["payment_method_id"]
#         payment_method_type = validated_data["payment_method_type"]

#         # Get the customer object for the logged in user
#         user = self.request.user
#         try:
#             customer = stripe.Customer.retrieve(user.stripe_customer_id)
#         except stripe.error.InvalidRequestError:
#             # Create a new customer object for the user
#             customer = stripe.Customer.create(email=user.email)
#             user.stripe_customer_id = customer.id
#             user.save()

#         # Attach the payment method to the customer if not already attached
#         payment_methods = stripe.PaymentMethod.list(
#             customer=customer.id,
#             type=payment_method_type,
#         )
#         if payment_method_id not in [pm.id for pm in payment_methods.data]:
#             payment_method = stripe.PaymentMethod.attach(payment_method_id, customer=customer.id)

#         # Calculate the end date of the subscription
#         end_date = timezone.now() + timedelta(days=30 * duration)

#         # Create a new subscription for the customer
#         subscription = stripe.Subscription.create(
#             customer=customer.id,
#             items=[{
#                 "price": plan
#             }],
#             default_payment_method=payment_method_id,
#             expand=["latest_invoice.payment_intent"],
#             trial_end=int(end_date.timestamp())
#         )

#         # Create a new payment intent for the subscription
#         payment_intent = stripe.PaymentIntent.create(
#             payment_method=payment_method_id,
#             customer=customer.id,
#             amount=amount,
#             currency="usd",
#             payment_method_types=[payment_method_type],
#             description="Payment for subscription to plan " + plan,
#             confirm=True,
#             receipt_email=customer.email,
#             metadata={'plan': plan},
#         )

#         # Get the payment intent object
#         payment_intent = stripe.PaymentIntent.retrieve(payment_intent.id)

#         # Update the subscription status based on the payment intent status
#         if payment_intent.status == "succeeded":
#             subscription = stripe.Subscription.retrieve(subscription.id)
#             subscription.save()
#         else:
#             subscription = stripe.Subscription.retrieve(subscription.id)
#             subscription.save()

#         # Create a new Subscription object
#         conduct_user = ConductUser.objects.get(email=user.email)
#         subscription_obj = Subscription.objects.create(
#             user=conduct_user,
#             plan=plan,
#             amount=amount,
#             stripe_subscription_id=subscription.id,
#             active=True,
#             expires_at=end_date
#         )

#         return Response({'subscription_id': subscription_obj.id}, status=status.HTTP_201_CREATED)

class PaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        request_data = request.data
        serializer = PaymentIntentSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        amount = validated_data["amount"]
        plan = validated_data["plan"]
        duration = validated_data["duration"]
        payment_method_id = validated_data["payment_method_id"]
        payment_method_type = validated_data["payment_method_type"]

        # Get the customer object for the logged in user
        user = self.request.user
        try:
            customer = stripe.Customer.retrieve(user.stripe_customer_id)
        except stripe.error.InvalidRequestError:
            # Create a new customer object for the user
            customer = stripe.Customer.create(email=user.email)
            user.stripe_customer_id = customer.id
            user.save()

        # Attach the payment method to the customer if not already attached
        payment_methods = stripe.PaymentMethod.list(
            customer=customer.id,
            type=payment_method_type,
        )
        if payment_method_id not in [pm.id for pm in payment_methods.data]:
            payment_method = stripe.PaymentMethod.attach(payment_method_id, customer=customer.id)

        # Calculate the end date of the subscription
        end_date = timezone.now() + timedelta(days=30 * duration)

        # Create a new subscription for the customer
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{
                "price": plan
            }],
            default_payment_method=payment_method_id,
            expand=["latest_invoice.payment_intent"],
            trial_end=int(end_date.timestamp())
        )

        # Create a new payment intent for the subscription
        payment_intent = stripe.PaymentIntent.create(
            payment_method=payment_method_id,
            customer=customer.id,
            amount=amount,
            currency="usd",
            payment_method_types=[payment_method_type],
            description="Payment for subscription to plan " + plan,
            confirm=True,
            receipt_email=customer.email,
            metadata={'plan': plan},
        )

        # Get the payment intent object
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent.id)

        # Handle requires_action status
        if payment_intent.status == "requires_action":
            # Send client_secret to client to handle authentication
            return Response({'client_secret': payment_intent.client_secret})

        # Update the subscription status based on the payment intent status
        if payment_intent.status == "succeeded":
            subscription = stripe.Subscription.retrieve(subscription.id)
            subscription.save()
        else:
            subscription = stripe.Subscription.retrieve(subscription.id)
            subscription.save()

        # Create a new Subscription object
        conduct_user = ConductUser.objects.get(email=user.email)
        subscription_obj = Subscription.objects.create(
            user=conduct_user,
            plan=plan,
            amount=amount,
            stripe_subscription_id=subscription.id,
            active=True,
            expires_at=end_date
        )

        return Response({'subscription_id': subscription_obj.id}, status=status.HTTP_201_CREATED)


