from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# --- User Account Management ---

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


# --- Profile and Healthcare Models ---

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    specialty = models.CharField(max_length=100, blank=True, null=True)
    medical_license_number = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    clinic_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.email}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_datetime = models.DateTimeField()
    appointment_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.email} for {self.patient.email}"


class MedicalDocument(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    s3_file_key = models.CharField(max_length=1024, unique=True)
    file_size = models.BigIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document '{self.file_name}' for {self.patient.email}"


class DocumentAccess(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_permissions')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_access')
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"Dr. {self.doctor.email} has access to {self.patient.email}'s records"
