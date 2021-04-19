from django.db import models


class RecordRSS(models.Model):
    published = models.DateTimeField("date published")
    link = models.CharField(max_length=256)
    description = models.CharField(max_length=4096)
    title = models.CharField(max_length=128)

    class Meta:
        db_table = "models_recordrss"