from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Patient, SystemNotification

@receiver(post_save, sender=Patient)
def log_new_patient_notification(sender, instance, created, **kwargs):
    if created:
        # Grabs the actual user full name linked to the newly registered patient profile
        patient_name = instance.user.get_full_name() if instance.user.first_name else instance.user.username
        
        # Saves a real alert log entry directly to our new notification table
        SystemNotification.objects.create(
            title="New Patient Admission",
            message=f"Patient {patient_name} has been successfully registered into the hospital database."
        )