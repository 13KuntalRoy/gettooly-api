from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import  timedelta
from accounts.models import  ConductUser
TYPE_CHOICES = (
        ('price_1NIqyoSJstE3ZNVNgNzVWHAc', _("A")),
        ('price_1NIr2TSJstE3ZNVNuK1U5LsH', _("A")),
        ('price_1N8e0kSJstE3ZNVNLmyt8xpP', _("B")),
        ('price_1N8e0kSJstE3ZNVNzjjm5OFl', _("B")),
        ('price_1N8e1bSJstE3ZNVNwgCZ4sKL', _("C")), 
        ('price_1N8e1bSJstE3ZNVNW6LQCFiH', _("C")),
        ('price_1N8e2BSJstE3ZNVN3ceChJtq', _("D")),
        ('price_1N8e2BSJstE3ZNVNcl64vI9B', _("D")),
    )


class Subscription(models.Model):
    user = models.ForeignKey(
    ConductUser, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.CharField(max_length=100, choices=TYPE_CHOICES, default="price_1NIqyoSJstE3ZNVNgNzVWHAc")
    amount = models.IntegerField()
    stripe_subscription_id = models.CharField(max_length=40, blank=True)
    active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=30))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan} - ${self.amount}"

    def save(self, *args, **kwargs):
        if self.plan == 'price_1NIqyoSJstE3ZNVNgNzVWHAc':
            self.plan = 'A'
        if self.plan == 'price_1NIr2TSJstE3ZNVNuK1U5LsH':
            self.plan = 'A'
        if self.plan == 'price_1N8e0kSJstE3ZNVNLmyt8xpP':
            self.plan = 'B'
        if self.plan == 'price_1N8e0kSJstE3ZNVNzjjm5OFl':
            self.plan = 'B'
        if self.plan == 'price_1N8e1bSJstE3ZNVNwgCZ4sKL':
            self.plan = 'C'
        if self.plan == 'price_1N8e1bSJstE3ZNVNW6LQCFiH':
            self.plan = 'C'
        if self.plan == 'price_1N8e2BSJstE3ZNVN3ceChJtq':
            self.plan = 'D'
        if self.plan == 'price_1N8e2BSJstE3ZNVNcl64vI9B':
            self.plan = 'D'
        super().save(*args, **kwargs)