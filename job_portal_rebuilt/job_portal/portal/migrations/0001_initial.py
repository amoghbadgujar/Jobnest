# Generated manually for a self-contained starter project.
from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('location', models.CharField(max_length=160)),
                ('job_type', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('internship', 'Internship'), ('contract', 'Contract'), ('freelance', 'Freelance')], default='full_time', max_length=20)),
                ('work_mode', models.CharField(choices=[('on_site', 'On-site'), ('hybrid', 'Hybrid'), ('remote', 'Remote')], default='on_site', max_length=20)),
                ('experience', models.CharField(choices=[('fresher', 'Fresher'), ('0_1', '0–1 years'), ('1_3', '1–3 years'), ('3_5', '3–5 years'), ('5_plus', '5+ years')], default='fresher', max_length=20)),
                ('skills', models.CharField(help_text='Comma-separated skills', max_length=500)),
                ('salary_min', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('salary_max', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('openings', models.PositiveIntegerField(default=1)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['title'], name='portal_job_title_65e0b2_idx'),
                    models.Index(fields=['location'], name='portal_job_locatio_3e15bb_idx'),
                    models.Index(fields=['job_type'], name='portal_job_job_typ_10d6a5_idx'),
                    models.Index(fields=['work_mode'], name='portal_job_work_mo_ae7b7d_idx'),
                    models.Index(fields=['created_at'], name='portal_job_created_27dce7_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('candidate', 'Candidate'), ('company', 'Company')], default='candidate', max_length=20)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('location', models.CharField(blank=True, max_length=120)),
                ('headline', models.CharField(blank=True, max_length=160)),
                ('bio', models.TextField(blank=True)),
                ('company_name', models.CharField(blank=True, max_length=160)),
                ('company_website', models.URLField(blank=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_by', to='portal.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_jobs', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-saved_at']},
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.TextField(blank=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='application_resumes/')),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('shortlisted', 'Shortlisted'), ('interview', 'Interview'), ('rejected', 'Rejected'), ('hired', 'Hired')], default='applied', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='portal.job')),
            ],
            options={'ordering': ['-applied_at']},
        ),
        migrations.AddConstraint(
            model_name='savedjob',
            constraint=models.UniqueConstraint(fields=('user', 'job'), name='unique_saved_job'),
        ),
        migrations.AddConstraint(
            model_name='application',
            constraint=models.UniqueConstraint(fields=('job', 'applicant'), name='unique_application'),
        ),
    ]
