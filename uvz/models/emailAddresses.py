from django.db import models


class EmailAddresses(models.Model):
    email = models.CharField(max_length=320)
    name = models.CharField(max_length=128, default="Undefined")

    class Meta(object):
        db_table = "email_addresses"
