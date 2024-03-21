from django.urls import path

from .views import UploadDataView, UserDataDetailView, UserUploadedCategoriesAPIView  # Importing views

urlpatterns = [
    path("upload-data/", UploadDataView.as_view(), name="upload-data"),  # URL pattern for uploading data
    path(
        "upload-data/<int:id>/", UserDataDetailView.as_view(), name="user_data_detail"
    ),  # URL pattern for viewing user data detail
    path("upload-categories/", UserUploadedCategoriesAPIView.as_view(), name="upload-categories"),  # URL pattern for uploading categories
]
