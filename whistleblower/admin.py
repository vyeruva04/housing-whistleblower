from django.contrib import admin
from .models import BuildingGroup
from .models import Complaint

# Register your models here.
admin.site.register(BuildingGroup)
admin.site.register(Complaint)
