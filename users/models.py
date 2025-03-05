from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Tambahkan field tambahan
    bio = models.TextField(_('bio'), blank=True, null=True)
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to='profile_pictures/',
        blank=True,
        null=True,
    )
    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return self.username