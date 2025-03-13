from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your models here.
class BuildingGroup(models.Model):
    name = models.CharField(max_length=50, null=False)
    User = get_user_model()
    users = models.ManyToManyField(User, null=True)


class Complaint(models.Model):
    class ComplaintType(models.IntegerChoices):
        NOISE_COMPLAINT = 1, "Noise Complaint"
        MESSINESS = 2, "Messiness"
        STOLEN_ITEM = 3, "Stolen Item"
        MAINTENANCE = 4, "Maintenance"
        PROPERTY_DAMAGE = 5, "Property Damage"
        PARKING_LOT = 6, "Parking Lot"
        LOITERING = 7, "Loitering"
        OTHER = 8, "Other"

    class ComplaintStatus(models.IntegerChoices):
        NEW = 1, "New"
        IN_PROGRESS = 2, "In Progress"
        RESOLVED = 3, "Resolved"

    # All Personal Information is Optional
    reporter = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    resolution_notes = models.TextField(max_length=500, null=True, blank=True)
    reporter_first_name = models.CharField(max_length=50, null=True, blank=True)
    reporter_last_name = models.CharField(max_length=50, null=True, blank=True)
    reporter_email = models.CharField(max_length=50, null=True, blank=True)
    # All Personal Information is Optional

    complaint_title = models.CharField(verbose_name="Title*", max_length=200)
    type_complaint = models.PositiveSmallIntegerField(
        choices=ComplaintType.choices, default=ComplaintType.NOISE_COMPLAINT, verbose_name="Complaint Type*")
    sent_date = models.DateTimeField("Date Sent", auto_now_add=True)
    incident_date = models.DateTimeField("Date of Incident*")
    respondent_name = models.CharField(max_length=50, null=True, blank= True, verbose_name="Respondent Name")
    location_address = models.CharField(max_length=50, verbose_name="Location Address*")
    location_description = models.TextField(max_length=500, verbose_name="Location Description*")
    incident_description = models.TextField(max_length=500, null=True, blank=True, verbose_name="Incident Description")
    # Need to work out how to upload and connect file upload
    file1 = models.FileField(upload_to="report_files", null=True, blank=True, verbose_name="File 1")
    file2 = models.FileField(upload_to="report_files", null=True, blank=True, verbose_name="File 2")
    file3 = models.FileField(upload_to="report_files", null=True, blank=True, verbose_name="File 3")
    additional_information = models.TextField(max_length=500, null=True, blank=True, verbose_name="Additional Information")
    urgency = models.IntegerField(verbose_name="How urgent from 1 to 5?*", default=1)
    complaint_status = models.PositiveSmallIntegerField(
        choices=ComplaintStatus.choices, default=ComplaintStatus.NEW)
    group = models.ForeignKey(BuildingGroup, on_delete=models.CASCADE, null=True, verbose_name="Building Group*")

    def complaint_status_phrase(self):
        status_mapping = {
            self.ComplaintStatus.NEW: "New",
            self.ComplaintStatus.IN_PROGRESS: "In Progress",
            self.ComplaintStatus.RESOLVED: "Resolved"
        }
        return status_mapping.get(self.complaint_status, "Unknown")

    def complaint_type_phrase(self):
        complaint_mapping = {
            self.ComplaintType.NOISE_COMPLAINT: "Noise Complaint",
            self.ComplaintType.MESSINESS:  "Messiness",
            self.ComplaintType.STOLEN_ITEM: "Stolen Item",
            self.ComplaintType.MAINTENANCE:  "Maintenance",
            self.ComplaintType.PROPERTY_DAMAGE: "Property Damage",
            self.ComplaintType.PARKING_LOT: "Parking Lot",
            self.ComplaintType.LOITERING: "Loitering",
            self.ComplaintType.OTHER: "Other"
        }
        return complaint_mapping.get(self.type_complaint, "Other")

    def delete(self, *args, **kwargs):
        self.file1.delete(save=False)
        self.file2.delete(save=False)
        self.file3.delete(save=False)
        super().delete(*args, **kwargs)

