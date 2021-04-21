from django.urls import path
from . import views


urlpatterns = [
    path("readRecords/", views.read_emails_from_database, name="Rea RSS record from database"), 
    path("insertRecord/", views.insert_record, name="DBInsert"),
    path("insertEmail/", views.insert_email, name="Insert email into database"), 
    path("deleteEmail/", views.delete_email, name="Delete email from database"),
    path("getEmails", views.read_emails_from_database, name="Retrieve emails from database")
]