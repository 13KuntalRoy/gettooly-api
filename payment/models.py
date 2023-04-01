import datetime

from django.db import models

from accounts.models import UserQuiz, ConductUser

class Subscription(models.Model):
    user = models.ForeignKey(
    ConductUser, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.CharField(max_length=20)
    amount = models.IntegerField()
    stripe_subscription_id = models.CharField(max_length=40, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan} - ${self.amount}"