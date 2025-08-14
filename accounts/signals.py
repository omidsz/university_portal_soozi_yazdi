from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserRole
from django.db.models.signals import post_delete


@receiver(post_save, sender=User)
def create_user_role(sender, instance, created, **kwargs):
    if created:
        UserRole.objects.get_or_create(user=instance, defaults={'role': 'user'})


@receiver(post_delete, sender=UserRole)
def delete_user_when_userrole_deleted(sender, instance, **kwargs):
    user = instance.user
    if user:
        user.delete()
