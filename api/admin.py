from django.contrib import admin
from .models import User, Profile, Appointment, MedicalDocument, DocumentAccess

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Appointment)
admin.site.register(MedicalDocument)
admin.site.register(DocumentAccess)
