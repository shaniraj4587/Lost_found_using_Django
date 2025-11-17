from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom User Model.
    We are extending the default Django User but making the 'username'
    field represent the "Roll No."
    """
    
    # We change the 'username' field's verbose_name to "Roll No."
    # This will change its label in forms and the admin.
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": "A user with that Roll No. already exists.",
        },
        verbose_name="Roll No." # This is the key change
    )

    # We can add other fields here if we want, like:
    # full_name = models.CharField(max_length=255, blank=True)
    # is_student = models.BooleanField(default=True)
    
    # We will use 'email' for password reset, so let's make it required.
    email = models.EmailField(unique=True, blank=False, null=False)

    # We want to log in with 'username' (Roll No.), so we keep this:
    USERNAME_FIELD = "username"
    
    # We need 'email' to be required for createsuperuser
    REQUIRED_FIELDS = ["email"] 

    def __str__(self):
        return self.username