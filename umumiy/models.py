from django.db import models

# Create your models here.

class user(models.Model):
    fullname = models.CharField( max_length=50)
    age = models.PositiveIntegerField()
    
    gmail = models.EmailField(max_length=254)
    password = models.CharField()


class uzbekGPT(models.Model):
    pass



class histories(models.Model):
    history = models.TextField()
    user_id = models.TextField()
    AI_agent_id = models.TextField()

    
    
