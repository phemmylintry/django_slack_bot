from django.urls import path

from .views import (
    DeleteFileView,
    Events,
    GetSingleFileView,
    ListOfMessage,
    UploadFileView,
)

urlpatterns = [
    path("", Events.as_view(), name="events"),
    path("list-messages/", ListOfMessage.as_view(), name="list-messages"),
    path("upload-file/", UploadFileView.as_view(), name="upload-file"),
    path("delete-file/", DeleteFileView.as_view(), name="delete-file"),
    path("get-single-file/", GetSingleFileView.as_view(), name="get-single-file"),
]
