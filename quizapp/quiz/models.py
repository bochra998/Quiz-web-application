from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Questions(models.Model):
    CAT_CHOICES = (
    ('Dogs','dogs'),
    ('Cats','cats'),
    )
    question = models.CharField(max_length = 250)
    optiona = models.CharField(max_length = 100)
    optionb = models.CharField(max_length = 100)
    optionc = models.CharField(max_length = 100)
    optiond = models.CharField(max_length = 100)
    answer = models.CharField(max_length = 100)
    catagory = models.CharField(max_length=20, choices = CAT_CHOICES)

    class Meta:
        ordering = ('-catagory',)

    def __str__(self):
        return self.question

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
