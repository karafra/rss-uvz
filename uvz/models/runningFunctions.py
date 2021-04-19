from django.db import models 


class RunningFunctions(models.Model):
    function_name = models.CharField(max_length=128)
    module_name = models.CharField(max_length=128)
    is_running = models.BooleanField()
