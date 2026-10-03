from django.contrib import admin

from .models import Application, Job, Profile, SavedJob


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'company_name', 'location', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'company_name')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'location', 'job_type', 'work_mode', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'job_type', 'work_mode', 'experience', 'is_featured', 'is_active')
    search_fields = ('title', 'location', 'skills', 'company__username')
    date_hierarchy = 'created_at'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('job__title', 'applicant__username', 'applicant__email')


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
