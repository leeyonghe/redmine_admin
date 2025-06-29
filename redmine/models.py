from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    identifier = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'projects'

class Issue(models.Model):
    PRIORITY_CHOICES = [
        (1, '낮음'),
        (2, '보통'),
        (3, '높음'),
        (4, '긴급'),
        (5, '즉시'),
    ]
    
    STATUS_CHOICES = [
        (1, '신규'),
        (2, '진행중'),
        (3, '해결됨'),
        (4, '피드백'),
        (5, '종료'),
        (6, '거부됨'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tracker_id = models.IntegerField()
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    status_id = models.IntegerField(choices=STATUS_CHOICES, default=1)
    assigned_to_id = models.IntegerField(null=True, blank=True)
    priority_id = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    author_id = models.IntegerField()
    lock_version = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    start_date = models.DateField(null=True, blank=True)
    done_ratio = models.IntegerField(default=0)
    estimated_hours = models.FloatField(null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    root_id = models.IntegerField(null=True, blank=True)
    lft = models.IntegerField(null=True, blank=True)
    rgt = models.IntegerField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    closed_on = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.subject
    
    class Meta:
        db_table = 'issues'

class TimeEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True)
    hours = models.FloatField()
    comments = models.CharField(max_length=255, blank=True)
    activity_id = models.IntegerField()
    spent_on = models.DateField()
    tyear = models.IntegerField()
    tmonth = models.IntegerField()
    tweek = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.hours}h"
    
    class Meta:
        db_table = 'time_entries'

class IssueStatus(models.Model):
    name = models.CharField(max_length=30)
    is_closed = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    position = models.IntegerField(default=1)
    default_done_ratio = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'issue_statuses'

class Tracker(models.Model):
    name = models.CharField(max_length=30)
    is_in_chlog = models.BooleanField(default=False)
    position = models.IntegerField(default=1)
    is_in_roadmap = models.BooleanField(default=True)
    fields_bits = models.IntegerField(default=0)
    default_status_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'trackers' 