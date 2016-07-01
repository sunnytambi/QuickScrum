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

    @property
    def get_issues_beneath(self):
        return Status_JiraIssue.objects.filter(status_id=self.status.id,
                                               status_particulars_id=self.id,
                                               status_type="Yesterday")

class TodayStatus(models.Model):
    status_text = models.TextField()
    status = models.ForeignKey(Status)

    @property
    def get_issues_beneath(self):
        return Status_JiraIssue.objects.filter(status_id=self.status.id,
                                               status_particulars_id=self.id,
                                               status_type="Today")

class IssueStatus(models.Model):
    status_text = models.TextField()
    status = models.ForeignKey(Status)

    @property
    def get_issues_beneath(self):
        return Status_JiraIssue.objects.filter(status_id=self.status.id,
                                               status_particulars_id=self.id,
                                               status_type="Issue")

class StatusTypes(models.Model):
    type = models.TextField()

class Status_JiraIssue(models.Model):
    status_type = models.TextField(default='Yesterday') #models.ForeignKey(StatusTypes)
    status = models.ForeignKey(Status)
    status_particulars_id = models.PositiveIntegerField(default=-1)
    jira_issue_id = models.TextField(default='')
    jira_issue_text = models.TextField(default='')
