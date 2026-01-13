from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from . models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new User is created
    Only for regular users (not staff/superuser)
    """
    if created:
        # Don't create profile for admin/staff users
        if not instance.is_staff and not instance.is_superuser:
            UserProfile. objects.create(
                user=instance,
                age=18,  # Default age - user will update later
                gender='other',  # Default gender
                height_cm=170,  # Default height
                weight_kg=70  # Default weight
            )
            print(f"✅ Auto-created profile for user: {instance.username}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the profile whenever the user is saved
    """
    # Only if profile exists (for staff users, profile might not exist)
    if hasattr(instance, 'profile'):
        instance.profile.save()
