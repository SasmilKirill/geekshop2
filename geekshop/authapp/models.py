from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


def get_activation_key_expiration_date():
    return now() + timedelta(days=2)


# Create your models here.
class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', blank=True, null=True)
    phone = models.CharField(
        max_length=20,
        verbose_name="телефон",
        blank=True,
    )
    city = models.CharField(max_length=20, verbose_name="город", blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(
        default=get_activation_key_expiration_date
    )

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        return True

    class ShopUserProfile(models.Model):
        MALE = 'M'
        FEMALE = 'W'

        GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

        user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)

        tagline = models.CharField(verbose_name='тэги', max_length=128, blank=True)

        about_me = models.TextField(verbose_name='о себе', max_length=512, blank=True)

        gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)

        @receiver(post_save, sender=ShopUser)
        def create_user_profile(sender, instance, created, **kwargs):
            if created:
                ShopUserProfile.objects.create(user=instance)

        @receiver(post_save, sender=ShopUser)
        def save_user_profile(sender, instance, **kwargs):
            instance.shopuserprofile.save()