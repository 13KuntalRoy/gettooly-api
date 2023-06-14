from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import  timedelta
from accounts.models import  ConductUser
TYPE_CHOICES = (
    ('free', _("A")),
    ('price_1N8e0kSJstE3ZNVNLmyt8xpP', _("B")),
    ('price_1N8e1bSJstE3ZNVNwgCZ4sKL', _("C")),
    ('price_1N8e2BSJstE3ZNVN3ceChJtq', _("D")),
)

class Subscription(models.Model):
    user = models.ForeignKey(
    ConductUser, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.CharField(max_length=100, choices=TYPE_CHOICES, default="free")
    amount = models.IntegerField()
    stripe_subscription_id = models.CharField(max_length=40, blank=True)
    active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=30))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan} - ${self.amount}"