import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Profile, Appointment, MedicalDocument, DocumentAccess
from .serializers import (
    UserSerializer,
    LoginSerializer,
    ProfileSerializer,
    DoctorPublicProfileSerializer,
    AppointmentSerializer,
    MedicalDocumentSerializer,
    DocumentAccessSerializer
)

# --- Auth Views ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# --- Appointment System Views ---
class DoctorListView(generics.ListAPIView):
    queryset = User.objects.filter(role='DOCTOR', profile__is_verified=True)
    serializer_class = DoctorPublicProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'PATIENT':
             raise serializers.ValidationError("Only patients can book appointments.")
        serializer.save(patient=self.request.user)

class MyAppointmentsListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'PATIENT':
            return Appointment.objects.filter(patient=user)
        elif user.role == 'DOCTOR':
            return Appointment.objects.filter(doctor=user)
        return Appointment.objects.none()

# --- Document Vault Views (NEW CODE) ---

class S3UploadRequestView(APIView):
    """
    An endpoint for patients to get a secure, pre-signed URL to upload a file to S3.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.role != 'PATIENT':
            return Response({"error": "Only patients can upload documents."}, status=status.HTTP_403_FORBIDDEN)

        file_name = request.data.get('file_name')
        file_type = request.data.get('file_type')
        if not file_name or not file_type:
            return Response({"error": "file_name and file_type are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # NOTE: In a real app, these credentials would be managed securely,
        # e.g., using IAM roles if running on EC2.
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        # The S3 key is the path to the file in the bucket
        object_key = f"documents/{request.user.id}/{file_name}"

        try:
            presigned_url = s3_client.generate_presigned_url(
                'put_object',
                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': object_key, 'ContentType': file_type},
                ExpiresIn=3600  # URL expires in 1 hour
            )
            return Response({'presigned_url': presigned_url, 's3_key': object_key})
        except ClientError as e:
            return Response({'error': 'Could not generate upload URL.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentCreateView(generics.CreateAPIView):
    """
    An endpoint for a patient to create a document record after uploading to S3.
    """
    serializer_class = MedicalDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class MyDocumentsListView(generics.ListAPIView):
    """
    An endpoint for a patient to see a list of their own documents.
    """
    serializer_class = MedicalDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MedicalDocument.objects.filter(patient=self.request.user)

class GrantDocumentAccessView(APIView):
    """
    An endpoint for a patient to grant a doctor access to their documents.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentAccessSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor_id = serializer.validated_data.get('doctor_id')
        try:
            doctor = User.objects.get(id=doctor_id, role='DOCTOR')
            DocumentAccess.objects.get_or_create(patient=request.user, doctor=doctor)
            return Response({'status': 'Access granted'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

