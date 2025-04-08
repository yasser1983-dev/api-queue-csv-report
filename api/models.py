from django.db import models

class TASMSMAESTRO(models.Model):
    name = models.CharField(max_length=255)
    date_report = models.DateField()

    class Meta:
        db_table = "TA_SMS_MAESTRO"

    def __str__(self):
        return f"{self.name} ({self.date})"


class TASMSDETALLE(models.Model):
    campaign = models.ForeignKey(TASMSMAESTRO, on_delete=models.CASCADE, related_name='details')
    message = models.TextField()
    receiver = models.CharField(max_length=20)

    class Meta:
        db_table = "TA_SMS_DETALLE"

    def __str__(self):
        return f"{self.receiver}: {self.message[:30]}"


class VirtualRQJob(models.Model):
    job_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(null=True, blank=True)
    enqueued_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    failure = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'api'  # Cambia esto según el nombre de tu aplicación

