from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

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
    
class Submission(models.Model):
    submission_id=models.CharField(max_length=255,primary_key=True,unique=True,editable=False)
    title=models.CharField(max_length=255)
    abstract=models.TextField
    keywords=models.TextField
    paper=models.FileField(upload_to="papers/")
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
