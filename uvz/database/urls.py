from django.urls import path
from . import views


urlpatterns = [
    path("readRecords", views.read_records_from_database, name="Index"), 
    path("insertRecord", views.insert_record, name="DBInsert"),
]