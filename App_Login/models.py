from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)
from django.conf import settings

class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, is_active=True, is_staff=False, is_admin=False):

        if not email:
            raise ValueError("User must have an Email-Address!")
        if not username:
            raise ValueError("User must have a Username!")
        if not password:
            raise ValueError("User must have a Password!")

        user_obj = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user_obj.staff  = is_staff
        user_obj.admin  = is_admin
        user_obj.active = is_active

        user_obj.set_password(password) # change user password
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
            is_staff=True
        )
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email         = models.EmailField(max_length=255, unique=True)
    username      = models.CharField(max_length=30, unique=True)
    active        = models.BooleanField(default=True)  # user can login
    staff         = models.BooleanField(default=False) # staff user non superuser
    admin         = models.BooleanField(default=False) # superuser
    timestamp     = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username',]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        ordering = ['-timestamp',]



class Profile(models.Model):
    GENDER_CHOICES = (
        ('Male' , 'Male'),
        ('Female' , 'Female'),
        ('Transgender' , 'Transgender'),
    )
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(default='default.png', upload_to='profile_pics')
    dob         = models.DateField(verbose_name="Date of Birth")
    gender      = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Male')
    website     = models.URLField(blank=True, null=True)
    linkedin    = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} following to {self.following.username}"









