from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta


class UserRole(models.Model):
    USER = 'user'
    MEMBER = 'member'
    MODERATOR = 'moderator'

    ROLE_CHOICES = [
        (USER, 'کاربر عادی'),
        (MEMBER, 'عضو انجمن'),
        (MODERATOR, 'مدیر انجمن'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class EmailVerificationCode(models.Model):
    email = models.EmailField(unique=True, default='omidszce@gmail.com')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"Code for {self.email}"
