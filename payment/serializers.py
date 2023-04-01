import datetime
import stripe
from payment.models import Subscription

from rest_framework import serializers

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            "id",
            "user",
            "plan",
            "amount",
            "stripe_subscription_id",
            "active",
            "created_at",
            "updated_at",
        )

class PaymentIntentSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    plan = serializers.CharField(max_length=20)
    duration = serializers.IntegerField(min_value=1, max_value=12)
    payment_method_id = serializers.CharField()
    payment_method_type = serializers.CharField()

    def create(self, validated_data):
        amount = validated_data["amount"]
        plan = validated_data["plan"]
        duration = validated_data["duration"]
        payment_method_id = validated_data["payment_method_id"]
        payment_method_type = validated_data["payment_method_type"]

        # Get the customer object for the logged in user
        user = self.context["request"].user
        customer = stripe.Customer.objects.get(user=user.stripe_customer_id)

        # Calculate the end date of the subscription
        end_date = datetime.now() + timedelta(days=30*duration)

        # Create a new subscription for the customer
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{
                "plan": plan
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

        # Create a new Subscription object
        subscription_obj = Subscription.objects.create(
            user=user,
            plan=plan,
            amount=amount,
            stripe_subscription_id=subscription.id,
            active=True,
            expires_at=end_date
        )

        return subscription_obj
