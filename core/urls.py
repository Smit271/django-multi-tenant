from django.urls import path

from .apiviews import SetDatabaseFileView


urlpatterns = [
    path("set_database_file/", SetDatabaseFileView.as_view(), name="set_database_file"),
]

