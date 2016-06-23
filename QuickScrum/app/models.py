"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    timestamp = models.DateTimeField()
    submitter = models.ForeignKey(User)

class YesterdayStatus(models.Model):
    status_text = models.TextField()
    status = models.ForeignKey(Status)

class TodayStatus(models.Model):
    status_text = models.TextField()
    status = models.ForeignKey(Status)

class IssueStatus(models.Model):
    status_text = models.TextField()
    status = models.ForeignKey(Status)
