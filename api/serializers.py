from rest_framework import serializers
from .models import User, Profile, Appointment, MedicalDocument, DocumentAccess

# --- User & Auth Serializers ---

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'profile_picture_url', 'specialty', 'clinic_address']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

# --- Appointment System Serializers ---

class DoctorPublicProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'profile']

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='DOCTOR'))
    patient = serializers.ReadOnlyField(source='patient.profile.full_name')

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_datetime', 'appointment_type', 'status']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['doctor'] = DoctorPublicProfileSerializer(instance.doctor).data
        return representation

# --- Document Vault Serializers (NEW CODE) ---

class MedicalDocumentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.profile.full_name', read_only=True)
    
    class Meta:
        model = MedicalDocument
        fields = ['id', 'patient_name', 'file_name', 'file_type', 's3_file_key', 'file_size', 'upload_date']
        read_only_fields = ['patient_name', 'upload_date'] # These are set by the system

class DocumentAccessSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()

