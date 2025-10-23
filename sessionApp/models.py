from django.db import models
from conferenceApp.models import Conference
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def clean(self):
        # Vérifier que la session est dans les dates de la conférence
        if self.conference and self.session_day:
            if not (self.Conference.start_date <= self.session_day <= self.Conference.end_date):
                raise ValidationError("La date de la session doit être comprise entre les dates de la conférence.")

        # Vérifier que l'heure de fin > heure de début
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")

    
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField
    start_time=models.TimeField
    end_time=models.TimeField
    room = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[A-Za-z0-9]+$', "Le nom de la salle ne doit contenir que lettres et chiffres.")]
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    conference=models.ForeignKey("conferenceApp.Conference",on_delete=models.CASCADE,related_name="sessions")
    #conference=models.ForeignKey(Conference,on_delete=models.CASCADE)
    