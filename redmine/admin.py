from django.contrib import admin
from .models import Project, Issue, TimeEntry, IssueStatus, Tracker, RedmineUser

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'status', 'created_on')
    list_filter = ('status', 'created_on')
    search_fields = ('name', 'description', 'identifier')
    ordering = ('-created_on',)

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('subject', 'project', 'status_id', 'priority_id', 'assigned_to_id', 'created_on')
    list_filter = ('status_id', 'priority_id', 'project', 'created_on')
    search_fields = ('subject', 'description')
    ordering = ('-created_on',)

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'issue', 'hours', 'spent_on')
    list_filter = ('project', 'spent_on', 'activity_id')
    search_fields = ('comments',)
    ordering = ('-spent_on',)

@admin.register(IssueStatus)
class IssueStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_closed', 'is_default', 'position')
    list_filter = ('is_closed', 'is_default')
    ordering = ('position',)

@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_in_roadmap', 'position')
    list_filter = ('is_in_roadmap',)
    ordering = ('position',)

@admin.register(RedmineUser)
class RedmineUserAdmin(admin.ModelAdmin):
    list_display = ('login', 'firstname', 'lastname', 'admin', 'status', 'last_login_on')
    list_filter = ('admin', 'status', 'created_on')
    search_fields = ('login', 'firstname', 'lastname')
    ordering = ('-created_on',) 