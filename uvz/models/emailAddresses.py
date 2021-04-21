from django.db import models

class EmailAddresses(models.Model):
    email = models.CharField(max_length=320)

    class Meta(object):
        db_table = "email_addresses"