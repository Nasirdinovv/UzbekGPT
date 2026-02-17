from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User_profile(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    
class Ai_agent(models.Model):
    name = models.CharField(max_length=255)
    kasbi = models.CharField(max_length=255)
    shaxsiyati = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.kasbi}"
    
class History(models.Model):

    FROM = [
        ("user", "User"),
        ("agent", "Agent")
    ]

    user = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    agent = models.ForeignKey(Ai_agent, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    kimdan = models.CharField(choices=FROM, max_length=10)

    def __str__(self):
        return f"{self.user.email} - {self.agent.name} - {self.timestamp}"