"""
Definition of models.
"""

from django.db import models

class YesterdayStatus(models.Model):
    status = models.TextField()

class TodayStatus(models.Model):
    status = models.TextField()

class IssueStatus(models.Model):
    status = models.TextField()
