from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import  timedelta
from accounts.models import  ConductUser
TYPE_CHOICES = (

    ('A', _("price_1NIqyoSJstE3ZNVNgNzVWHAc")),
    ('A',_("price_1NIr2TSJstE3ZNVNuK1U5LsH")),
    ('B',_("price_1N8e0kSJstE3ZNVNLmyt8xpP")),
    ('B',_("price_1N8e0kSJstE3ZNVNzjjm5OFl")),
    ('C',_("price_1N8e1bSJstE3ZNVNwgCZ4sKL")), 
    ('C',_("price_1N8e1bSJstE3ZNVNW6LQCFiH")),
    ('D',_("price_1N8e2BSJstE3ZNVN3ceChJtq")),
    ('D',_("price_1N8e2BSJstE3ZNVNcl64vI9B")),
)

class Subscription(models.Model):
    user = models.ForeignKey(
    ConductUser, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.CharField(max_length=100, choices=TYPE_CHOICES, default="A")
    amount = models.IntegerField()
    stripe_subscription_id = models.CharField(max_length=40, blank=True)
    active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=30))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan} - ${self.amount}"