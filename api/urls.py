from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    ProfileView,
    DoctorListView,
    AppointmentCreateView,
    MyAppointmentsListView,
    S3UploadRequestView,
    DocumentCreateView,
    MyDocumentsListView,
    GrantDocumentAccessView
)

urlpatterns = [
    # --- Auth Endpoints ---
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # --- Appointment System Endpoints ---
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('appointments/book/', AppointmentCreateView.as_view(), name='appointment-book'),
    path('appointments/my-appointments/', MyAppointmentsListView.as_view(), name='my-appointments'),

    # --- Document Vault Endpoints ---
    path('documents/upload-request/', S3UploadRequestView.as_view(), name='s3-upload-request'),
    path('documents/create-record/', DocumentCreateView.as_view(), name='document-create-record'),
    path('documents/my-documents/', MyDocumentsListView.as_view(), name='my-documents'),
    path('documents/grant-access/', GrantDocumentAccessView.as_view(), name='grant-document-access'),
]

