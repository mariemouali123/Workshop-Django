from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
import datetime
import re
import uuid
from datetime import date
from django.core.validators import FileExtensionValidator
from Userapp.models import User

# Create your models here.
class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    THEME=[
        ("IA","computer science & ia"),
        ("SE","Science & Engineering"),
        ("SC","Social Scuences & Education"),
        ("IT","Interdisciplinary Themes"),
    ]
    theme=models.CharField(max_length=255,choices=THEME)
    location=models.CharField(max_length=50)
    description=models.TextField(validators=[MinLengthValidator(30,"minimum 30 caracteres")])
    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"la conference a comme titre {self.name}"
    
    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("La date de debut de la conference doit etre inferieur a la date de fin")
            
    def validate_title(value):
    #Titre sans chiffres ni caractères spéciaux.
        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", value):
            raise ValidationError("Le titre ne doit contenir que des lettres et espaces.")
        
    
    def validate_keywords(value):
    #Vérifie que le nombre de mots-clés séparés par des virgules ne dépasse pas 10.
        keywords = [k.strip() for k in value.split(',') if k.strip()]
        if len(keywords) > 10:
            raise ValidationError("Vous ne pouvez pas avoir plus de 10 mots-clés.")
        
    
    
class Submission(models.Model):
    submission_id=models.CharField(max_length=255,primary_key=True,unique=True,editable=False)
    title = models.CharField(max_length=200, validators=[validate_title])
    abstract=models.TextField
    keywords = models.CharField(max_length=255, validators=[validate_keywords])
    paper = models.FileField(
        upload_to='papers/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    STATUS=[
        ("submitted","submitted"),
        ("under review","under review"),
        ("accepted","accepted"),
        ("rejected","rejected"),
    ]
    status=models.CharField(max_length=255,choices=STATUS)
    payed=models.BooleanField(default=False)
    submissions_date=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey("Userapp.User",on_delete=models.CASCADE,related_name="submissions")
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="submissions")
    user = models.ForeignKey('Userapp.User', on_delete=models.CASCADE)

    def clean(self):
        # 1️⃣ Conférence à venir
        if self.conference and self.conference.start_date < date.today():
            raise ValidationError("La soumission ne peut être faite que pour des conférences à venir.")

        # 2️⃣ Maximum 3 soumissions par jour par utilisateur
        if self.user and self.submission_date:
            count_today = Submission.objects.filter(
                user=self.user,
                submission_date=date.today()
            ).count()
            if count_today >= 3:
                raise ValidationError("Vous ne pouvez pas soumettre plus de 3 conférences par jour.")

    # --- ID AUTOMATIQUE ---
    def save(self, *args, **kwargs):
        if not self.submission_id:
            # Génère un ID du type SUBABCDEFGH
            self.submission_id = f"SUB{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.conference.title})"
    

class OrganizingCommittee(models.Model):
    COMMITTEE_ROLES=[
        ("chair","chair"),
        ("co-chair","co-chair"),
        ("member","member")
    ]
    committee_role=models.CharField(max_length=255,choices=COMMITTEE_ROLES)
    date_joined=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey("Userapp.User",on_delete=models.CASCADE,related_name="committee")
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="committee")
