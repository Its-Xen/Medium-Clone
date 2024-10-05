import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from core_apps.profiles.models import Profile

logger = logging.getLogger(__name__)

User = get_user_model()  # This will use our custom "users.User" model

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"{instance}'s profile has been created!")
