from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    ROLE_CHOICES = [('candidate', 'Candidate'), ('company', 'Company')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=120, blank=True)
    headline = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    company_name = models.CharField(max_length=160, blank=True)
    company_website = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'


class Job(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('design', 'Design'),
        ('data', 'Data & Analytics'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('content', 'Content & Writing'),
        ('it_support', 'IT Support'),
        ('operations', 'Operations'),
        ('management', 'Management'),
        ('human_resources', 'Human Resources'),
        ('customer_service', 'Customer Service'),
    ]
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
    ]
    WORK_MODE_CHOICES = [('on_site', 'On-site'), ('hybrid', 'Hybrid'), ('remote', 'Remote')]
    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher'),
        ('0_1', '0–1 years'),
        ('1_3', '1–3 years'),
        ('3_5', '3–5 years'),
        ('5_plus', '5+ years'),
    ]

    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='technology')
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=160)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, default='on_site')
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    skills = models.CharField(max_length=500, help_text='Comma-separated skills')
    salary_min = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    salary_max = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    openings = models.PositiveIntegerField(default=1)
    deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['location']),
            models.Index(fields=['job_type']),
            models.Index(fields=['category']),
            models.Index(fields=['work_mode']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return bool(self.deadline and self.deadline < timezone.localdate())

    @property
    def skill_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    @property
    def company_display_name(self):
        profile = getattr(self.company, 'profile', None)
        return profile.company_name if profile and profile.company_name else self.company.get_full_name() or self.company.username


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'job'], name='unique_saved_job')]
        ordering = ['-saved_at']


class JobAlert(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    email = models.EmailField()
    keyword = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=120, blank=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='weekly')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['email', 'keyword', 'location'], name='unique_job_alert')
        ]

    def __str__(self):
        parts = [self.keyword or 'Any role', self.location or 'Any location']
        return ' | '.join(filter(None, parts))


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['job', 'applicant'], name='unique_application')]
        ordering = ['-applied_at']

    def __str__(self):
        return f'{self.applicant.username} → {self.job.title}'
