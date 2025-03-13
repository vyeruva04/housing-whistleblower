from django import forms

from .models import Complaint
from .models import BuildingGroup

from django.utils import timezone

N_COMPLAINT_CHOICES = (
    (1, "Noise Complaint"),
    (2, "Messiness"),
    (8, "Other"),
)

B_COMPLAINT_CHOICES = (
    (3, "Stolen Item"),
    (4, "Maintenance"),
    (5, "Property Damage"),
    (6, "Parking Lot"),
    (7, "Loitering"),
    (8, "Other"),
)
# class NeighborComplaintForm(forms.Form):
#     reporter_first_name = forms.CharField(label="First Name", max_length=50, required=False)
#     reporter_last_name = forms.CharField(label="Last Name", max_length=50, required=False)
#     reporter_phone_number = forms.CharField(label="Phone Number", max_length=12, required=False)
#     reporter_email = forms.CharField(label = "Email", max_length=50, required=False)
#     reporter_description = forms.CharField(label = "Relationship To The Incident and Reportee", max_length=400, required=False, widget=forms.Textarea)
#
#     complaint_title = forms.CharField(label="Subject", max_length=200, widget=forms.Textarea)
#     type_complaint = forms.ChoiceField(label = "Complaint Type", choices=N_COMPLAINT_CHOICES)
#     sent_date = forms.DateTimeField(label = "Date Sent")
#     incident_date = forms.DateTimeField(label = "Date of Incident")
#     respondent_name = forms.CharField(label = "Reportee's Name", max_length=50, required=False)
#     respondent_location = forms.CharField(label = "Reportee's Address", max_length=200, required=False, widget=forms.Textarea)
#     location_address = forms.CharField(label = "Address of Incident", max_length=50)
#     location_description = forms.CharField(label = "Description of Place of Incident", max_length=500, widget=forms.Textarea)
#     incident_description = forms.CharField(label = "Description of Incident", max_length=500, widget=forms.Textarea)
#     # # Need to work out how to upload and connect file upload
#     # # file1 = models.FileField(upload_to="report_files", blank=True)
#     # # file2 = models.FileField(upload_to="report_files", blank=True)
#     # # file3 = models.FileField(upload_to="report_files", blank=True)
#     additional_information = forms.CharField(max_length=500, required=False, widget=forms.Textarea)
#     expected_completion = forms.DateTimeField(label = "How urgent?", required=False)

# class BuildingComplaintForm(forms.Form):
#     reporter_first_name = forms.CharField(label="First Name", max_length=50, required=False)
#     reporter_last_name = forms.CharField(label="Last Name", max_length=50, required=False)
#     reporter_phone_number = forms.CharField(label="Phone Number", max_length=12, required=False)
#     reporter_email = forms.CharField(label="Email", max_length=50, required=False)
#     reporter_description = forms.CharField(label="Relationship To The Incident and Reportee", max_length=400,
#                                            required=False, widget=forms.Textarea)
#
#     complaint_title = forms.CharField(label="Subject", max_length=200, widget=forms.Textarea)
#     type_complaint = forms.ChoiceField(label="Complaint Type", choices=B_COMPLAINT_CHOICES)
#     sent_date = forms.DateTimeField(label="Date Sent")
#     incident_date = forms.DateTimeField(label="Date of Incident")
#     respondent_name = forms.CharField(label="Reportee's Name", max_length=50, required=False)
#     respondent_location = forms.CharField(label="Reportee's Address", max_length=200, required=False,
#                                           widget=forms.Textarea)
#     location_address = forms.CharField(label="Address of Incident", max_length=50)
#     location_description = forms.CharField(label="Description of Place of Incident", max_length=500,
#                                            widget=forms.Textarea)
#     incident_description = forms.CharField(label="Description of Incident", max_length=500, widget=forms.Textarea)
#     # # Need to work out how to upload and connect file upload
#     file1 = forms.FileField(label="File Upload", required=False)
#     file2 = forms.FileField(label="File Upload", required=False)
#     file3 = forms.FileField(label="File Upload", required=False)
#     additional_information = forms.CharField(max_length=500, required=False, widget=forms.Textarea)
#     expected_completion = forms.DateTimeField(label="How urgent?", required=False)

class BComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ["complaint_status", "resolution_notes", "sent_date",
                   "reporter_first_name", "reporter_last_name",
                   "reporter_email", "reporter", "respondent_name"
                   ]

        widgets = {
            'incident_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def __init__(self, user, *args, **kwargs):
        super(BComplaintForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = BuildingGroup.objects.filter(users=user)
        self.fields['group'].label_from_instance = lambda instance: instance.name
    def clean_urgency(self):
        data = self.cleaned_data["urgency"]
        if data < 1 or data > 5:
            raise forms.ValidationError("Please enter a value between 1 and 5")
        return data
    def clean_incident_date(self):
        data = self.cleaned_data["incident_date"]
        if data > timezone.now():
            raise forms.ValidationError("Date cannot be in the future")
        return data
    
class NComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ["complaint_status", "resolution_notes", "sent_date",
                   "reporter_first_name", "reporter_last_name", "reporter_email", "reporter"
                   ]
        widgets = {
            'incident_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(NComplaintForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = BuildingGroup.objects.filter(users=user)
        self.fields['group'].label_from_instance = lambda instance: instance.name


    def clean_urgency(self):
        data = self.cleaned_data["urgency"]
        if data < 1 or data > 5:
            raise forms.ValidationError("Please enter a value between 1 and 5")
        return data

    def clean_incident_date(self):
        data = self.cleaned_data["incident_date"]
        if data > timezone.now():
            raise forms.ValidationError("Date cannot be in the future")
        return data

class ANComplaintForm(forms.ModelForm):

    groupField = forms.IntegerField(label="Building Code*", required=True)
    class Meta:

        model = Complaint
        exclude = [
            "complaint_status", "resolution_notes", "sent_date",
            "reporter", "reporter_first_name", "reporter_last_name",
            "reporter_email", "group"
        ]

        widgets = {
            'incident_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_groupField(self):
        data = self.cleaned_data["groupField"]
        if not BuildingGroup.objects.filter(id=data).exists():
            raise forms.ValidationError("Building Code is not valid")
        return data
    def clean_urgency(self):
        data = self.cleaned_data["urgency"]
        if data < 1 or data > 5:
            raise forms.ValidationError("Please enter a value between 1 and 5")
        return data

    def clean_incident_date(self):
        data = self.cleaned_data["incident_date"]
        if data > timezone.now():
            raise forms.ValidationError("Date cannot be in the future")
        return data

class ABComplaintForm(forms.ModelForm):

    groupField = forms.IntegerField(label="Building Code*", required=True)
    class Meta:

        model = Complaint
        exclude = [
            "complaint_status", "resolution_notes", "sent_date",
            "reporter", "reporter_first_name", "reporter_last_name",
            "reporter_email", "group", "respondent_name"
        ]

        widgets = {
            'incident_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_groupField(self):
        data = self.cleaned_data["groupField"]
        if not BuildingGroup.objects.filter(id=data).exists():
            raise forms.ValidationError("Building Code is not valid")
        return data
    def clean_urgency(self):
        data = self.cleaned_data["urgency"]
        if data < 1 or data > 5:
            raise forms.ValidationError("Please enter a value between 1 and 5")
        return data

    def clean_incident_date(self):
        data = self.cleaned_data["incident_date"]
        if data > timezone.now():
            raise forms.ValidationError("Date cannot be in the future")
        return data
