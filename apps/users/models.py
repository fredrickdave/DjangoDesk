from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # https://docs.djangoproject.com/en/4.2/topics/db/models/#abstract-base-classes
    class Meta:
        abstract = True


class UserRole(BaseModel):
    class Role(models.IntegerChoices):
        ADMIN = "1", "Administrator"
        AGENT = "2", "Support Agent"
        CUSTOMER = "3", "Customer"

    role = models.IntegerField(choices=Role.choices, null=True, blank=True)

    def __str__(self) -> str:
        # https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.get_FOO_display
        return self.get_role_display()


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices
    class Role(models.TextChoices):
        ADMIN = "Admin", "Administrator"
        AGENT = "Agent", "Support Agent"
        CUSTOMER = "Customer", "Customer"

    username = None
    email = models.EmailField(unique=True)
    # role = models.TextField(choices=Role.choices, null=True, blank=True)
    role = models.ForeignKey(UserRole, null=True, blank=True, on_delete=models.SET_NULL, related_name="users")

    # https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.models.CustomUser
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.get_username()
