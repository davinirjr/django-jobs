from django.db import models


class Job(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='PENDING', max_length=30)
    info = models.CharField(default='', max_length=30)
