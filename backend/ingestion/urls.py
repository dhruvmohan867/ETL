from django.urls import path
from .views import FileUploadView

urlpatterns = [
    path('<str:source_type>/', FileUploadView.as_view(), name='file-upload'),
]
