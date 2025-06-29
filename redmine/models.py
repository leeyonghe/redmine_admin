from django.db import models
# from django.contrib.auth.models import User  # No longer needed

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    homepage = models.CharField(max_length=255, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    parent_id = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    identifier = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(default=1)
    lft = models.IntegerField(null=True, blank=True)
    rgt = models.IntegerField(null=True, blank=True)
    inherit_members = models.BooleanField(default=False)
    default_version_id = models.IntegerField(null=True, blank=True)
    default_assigned_to_id = models.IntegerField(null=True, blank=True)
    
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
    
    tracker_id = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    author_id = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey('RedmineUser', on_delete=models.CASCADE, db_column='user_id')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True, db_column='issue_id')
    hours = models.FloatField()
    comments = models.CharField(max_length=1024, blank=True, null=True)
    activity_id = models.IntegerField()
    spent_on = models.DateField()
    tyear = models.IntegerField()
    tmonth = models.IntegerField()
    tweek = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.login} - {self.hours}h"
    
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
    description = models.CharField(max_length=255, blank=True, null=True)
    position = models.IntegerField(default=1)
    is_in_roadmap = models.BooleanField(default=True)
    fields_bits = models.IntegerField(default=0)
    default_status_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'trackers'

class RedmineUser(models.Model):
    login = models.CharField(max_length=255)
    hashed_password = models.CharField(max_length=40)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=255)
    admin = models.BooleanField(default=False)
    status = models.IntegerField(default=1)
    last_login_on = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=5, blank=True, null=True)
    auth_source_id = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    mail_notification = models.CharField(max_length=255, default='')
    salt = models.CharField(max_length=64, blank=True, null=True)
    must_change_passwd = models.BooleanField(default=False)
    passwd_changed_on = models.DateTimeField(null=True, blank=True)
    twofa_scheme = models.CharField(max_length=255, blank=True, null=True)
    twofa_totp_key = models.CharField(max_length=255, blank=True, null=True)
    twofa_totp_last_used_at = models.IntegerField(null=True, blank=True)
    twofa_required = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        db_table = 'users' 