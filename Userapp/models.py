from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.

def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()

def verify_email(email):
    domaines=["esprit.tn","sesame.com","tek.tn","central.net"]
    email_domaine=email.split("@")[1]
    if email_domaine not in domaines:
        raise ValidationError("l'email est invalide et doit appartenir a une universite")

name_validator=RegexValidator(
    regex='^[a-zA-Z\s-]+$',  #\s ca veut dire un espace
    message="ce champ ne doit contenir que des lettres et des espaces"
)
class User(AbstractUser):
    user_id=models.CharField(max_length=8,primary_key=True,unique=True,editable=False)
    first_name=models.CharField(max_length=255,validators=[name_validator])
    last_name=models.CharField(max_length=255,validators=[name_validator])
    affiliation=models.CharField(max_length=255)
    role=models.CharField(max_length=255)
    ROLE=[
        ("participant","participant"),
        ("commitee","organizing commitee member"),
    ]
    role=models.CharField(max_length=255,choices=ROLE,default="participant")
    email=models.EmailField(unique=True,validators=[verify_email])
    nationality=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
        if not self.user_id:
            newid=generate_user_id()
            while User.objects.filter(user_id=newid).exists():
                newid=generate_user_id()
            self.user_id=newid
        super().save(*args,**kwargs)


