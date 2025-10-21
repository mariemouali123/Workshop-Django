from django.db import models
from conferenceApp.models import Conference
from django.core.exceptions import ValidationError

def assert_in_range(value, start_date, end_date, field_name="session_day"):
    if value is None or start_date is None or end_date is None:
        return
    if not (start_date <= value <= end_date):
        raise ValidationError({field_name: "La date de la session doit appartenir à l’intervalle de la conférence."})

    
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField
    start_time=models.TimeField
    end_time=models.TimeField
    room=models.CharField
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    conference=models.ForeignKey("conferenceApp.Conference",on_delete=models.CASCADE,related_name="sessions")
    #conference=models.ForeignKey(Conference,on_delete=models.CASCADE)
    