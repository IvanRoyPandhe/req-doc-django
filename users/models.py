from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

class CustomUser(AbstractUser):
    # Override username field to remove character restrictions
    username = models.CharField(
        _('username'),
        max_length=255,  
        unique=True,
        help_text=_('Required. 255 characters or fewer.'),
        validators=[MinLengthValidator(1)],  
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

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