from django.urls import path

from .views import (
    DeleteFileView,
    Events,
    GetSingleFileView,
    ListOfMessage,
    UploadFileView,
)

urlpatterns = [
    path("", Events.as_view()),
    path("list-messages/", ListOfMessage.as_view()),
    path("upload-file/", UploadFileView.as_view()),
    path("delete-file/", DeleteFileView.as_view()),
    path("get-single-file/", GetSingleFileView.as_view()),
]
