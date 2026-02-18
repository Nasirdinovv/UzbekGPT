from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# <<< User_profile modellari >>> #
class UserProfile(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
# <<< Ai_agent modellari >>> #    
class Ai_agent(models.Model):
    name = models.CharField(max_length=100)
    kasbi = models.CharField(max_length=100)
    shaxsiyati = models.TextField()
    icon = models.CharField(max_length=255)  # Ikonka URL'si
    def __str__(self):
        return f"{self.name} - {self.kasbi}"
    


# <<< History modellari >>> #
class History(models.Model):
    KIMDAN = [
        ('user', 'User'),
        ('agent', 'Agent'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agent = models.ForeignKey(Ai_agent, on_delete=models.CASCADE)
    text = models.TextField()

    kimdan = models.CharField(choices=KIMDAN, max_length=10)

    def __str__(self):
        return f"{self.user.email} - {self.agent.name} - {self.kasi }"
    



class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mode = models.CharField(max_length=50)  # Matematika, Tarix, va h.k.
    title = models.CharField(max_length=255) # Suhbat mavzusi (tarix uchun)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    is_bot = models.BooleanField(default=False)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)