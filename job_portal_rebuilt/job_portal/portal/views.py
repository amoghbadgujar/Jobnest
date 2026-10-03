from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ApplicationForm, JobAlertForm, JobForm, ProfileForm, RegisterForm
from .models import Application, Job, JobAlert, Profile, SavedJob


def get_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def home(request):
    base_qs = Job.objects.filter(is_active=True).select_related('company', 'company__profile')
    featured_jobs = base_qs.filter(is_featured=True)[:8]
    latest_jobs = base_qs.filter(is_featured=False)[:6]
    job_count = base_qs.count()
    company_count = User.objects.filter(jobs__isnull=False, profile__role='company').distinct().count()
    category_counts = []
    for value, label in Job.CATEGORY_CHOICES:
        category_counts.append((value, label, base_qs.filter(category=value).count()))
    showcase_jobs = list(featured_jobs) + list(latest_jobs)
    saved_ids = set()
    applied_ids = set()
    if request.user.is_authenticated:
        saved_ids = set(SavedJob.objects.filter(user=request.user, job__in=showcase_jobs).values_list('job_id', flat=True))
        applied_ids = set(Application.objects.filter(applicant=request.user, job__in=showcase_jobs).values_list('job_id', flat=True))
    return render(request, 'portal/home.html', {
        'featured_jobs': featured_jobs, 'latest_jobs': latest_jobs,
        'job_count': job_count, 'company_count': company_count,
        'category_counts': category_counts, 'saved_ids': saved_ids, 'applied_ids': applied_ids,
        'job_alert_form': JobAlertForm(),
    })


def company_directory(request):
    companies = User.objects.filter(profile__role='company').select_related('profile').annotate(
        active_jobs=Count('jobs', filter=Q(jobs__is_active=True)),
        total_jobs=Count('jobs')
    ).order_by('-active_jobs', '-total_jobs', 'username')
    return render(request, 'portal/company_directory.html', {'companies': companies})


def job_alerts(request):
    form = JobAlertForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'You are subscribed for job alerts.')
        return redirect('portal:job_list')
    return render(request, 'portal/job_alerts.html', {'form': form})


def job_list(request):
    qs = Job.objects.filter(is_active=True).select_related('company', 'company__profile')
    q = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    job_type = request.GET.get('job_type', '').strip()
    work_mode = request.GET.get('work_mode', '').strip()
    experience = request.GET.get('experience', '').strip()
    category = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', 'newest')

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(skills__icontains=q) | Q(description__icontains=q) | Q(company__profile__company_name__icontains=q))
    if location:
        qs = qs.filter(location__icontains=location)
    if job_type:
        qs = qs.filter(job_type=job_type)
    if work_mode:
        qs = qs.filter(work_mode=work_mode)
    if experience:
        qs = qs.filter(experience=experience)
    if category:
        qs = qs.filter(category=category)

    if sort == 'salary_high':
        qs = qs.order_by('-salary_max', '-salary_min', '-created_at')
    elif sort == 'salary_low':
        qs = qs.order_by('salary_min', 'salary_max', '-created_at')
    elif sort == 'oldest':
        qs = qs.order_by('created_at')
    else:
        qs = qs.order_by('-created_at')

    jobs = list(qs[:100])
    saved_ids = set()
    applied_ids = set()
    if request.user.is_authenticated:
        saved_ids = set(SavedJob.objects.filter(user=request.user, job__in=jobs).values_list('job_id', flat=True))
        applied_ids = set(Application.objects.filter(applicant=request.user, job__in=jobs).values_list('job_id', flat=True))

    return render(request, 'portal/job_list.html', {
        'jobs': jobs,
        'saved_ids': saved_ids,
        'applied_ids': applied_ids,
        'filters': {
            'q': q, 'location': location, 'job_type': job_type,
            'work_mode': work_mode, 'experience': experience, 'category': category, 'sort': sort,
        },
        'job_type_choices': Job.JOB_TYPE_CHOICES,
        'category_choices': Job.CATEGORY_CHOICES,
        'sort_choices': [
            ('newest', 'Newest first'),
            ('salary_high', 'Salary: High to low'),
            ('salary_low', 'Salary: Low to high'),
            ('oldest', 'Oldest first'),
        ],
    })


def job_detail(request, pk):
    job = get_object_or_404(Job.objects.select_related('company', 'company__profile'), pk=pk)
    related_jobs = Job.objects.filter(is_active=True).exclude(pk=job.pk).filter(location__icontains=job.location.split(',')[0])[:4]
    already_applied = request.user.is_authenticated and Application.objects.filter(job=job, applicant=request.user).exists()
    is_saved = request.user.is_authenticated and SavedJob.objects.filter(job=job, user=request.user).exists()
    return render(request, 'portal/job_detail.html', {
        'job': job,
        'related_jobs': related_jobs,
        'already_applied': already_applied,
        'is_saved': is_saved,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('portal:dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully.')
        return redirect('portal:dashboard')
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    profile = get_profile(request.user)
    if profile.role == 'company':
        jobs = Job.objects.filter(company=request.user)
        applications = Application.objects.filter(job__company=request.user).select_related('job', 'applicant')
        context = {
            'profile': profile,
            'jobs': jobs[:8],
            'total_jobs': jobs.count(),
            'active_jobs': jobs.filter(is_active=True).count(),
            'total_applications': applications.count(),
            'recent_applications': applications[:8],
        }
        return render(request, 'portal/company_dashboard.html', context)

    applications = Application.objects.filter(applicant=request.user).select_related('job', 'job__company', 'job__company__profile')
    saved = SavedJob.objects.filter(user=request.user).select_related('job', 'job__company', 'job__company__profile')
    context = {
        'profile': profile,
        'application_count': applications.count(),
        'saved_count': saved.count(),
        'recent_applications': applications[:6],
        'saved_jobs': saved[:6],
    }
    return render(request, 'portal/candidate_dashboard.html', context)


@login_required
def profile(request):
    profile = get_profile(request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated.')
        return redirect('portal:profile')
    return render(request, 'portal/profile.html', {'form': form, 'profile': profile})


@login_required
def apply_job(request, job_id):
    profile = get_profile(request.user)
    if profile.role != 'candidate':
        messages.error(request, 'Only candidate accounts can apply for jobs.')
        return redirect('portal:job_detail', pk=job_id)
    job = get_object_or_404(Job, pk=job_id, is_active=True)
    if job.is_expired:
        messages.error(request, 'This application deadline has passed.')
        return redirect('portal:job_detail', pk=job.id)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, 'You already applied for this job.')
        return redirect('portal:job_detail', pk=job.id)

    form = ApplicationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.job = job
        application.applicant = request.user
        if not application.resume and profile.resume:
            application.resume = profile.resume
        application.save()
        messages.success(request, 'Application submitted successfully.')
        return redirect('portal:my_applications')
    return render(request, 'portal/apply.html', {'form': form, 'job': job, 'profile': profile})


@login_required
def toggle_save_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, is_active=True)
    if SavedJob.objects.filter(job=job, user=request.user).exists():
        SavedJob.objects.filter(job=job, user=request.user).delete()
        saved = False
    else:
        SavedJob.objects.create(job=job, user=request.user)
        saved = True
    if request.headers.get('HX-Request') or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'saved': saved})
    messages.success(request, 'Job saved.' if saved else 'Job removed from saved jobs.')
    return redirect(request.META.get('HTTP_REFERER', '/jobs/'))


@login_required
def create_job(request):
    profile = get_profile(request.user)
    if profile.role != 'company':
        messages.error(request, 'Only company accounts can post jobs.')
        return redirect('portal:dashboard')
    form = JobForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        job = form.save(commit=False)
        job.company = request.user
        job.save()
        messages.success(request, 'Job posted successfully.')
        return redirect('portal:dashboard')
    return render(request, 'portal/job_form.html', {'form': form, 'mode': 'Create', 'profile': profile})


@login_required
def edit_job(request, job_id):
    profile = get_profile(request.user)
    if profile.role != 'company':
        return redirect('portal:dashboard')
    job = get_object_or_404(Job, pk=job_id, company=request.user)
    form = JobForm(request.POST or None, instance=job)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Job updated successfully.')
        return redirect('portal:dashboard')
    return render(request, 'portal/job_form.html', {'form': form, 'mode': 'Edit', 'job': job, 'profile': profile})


@login_required
def delete_job(request, job_id):
    profile = get_profile(request.user)
    if profile.role != 'company':
        return redirect('portal:dashboard')
    job = get_object_or_404(Job, pk=job_id, company=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted.')
        return redirect('portal:dashboard')
    return render(request, 'portal/confirm_delete.html', {'job': job})


@login_required
def company_applications(request):
    profile = get_profile(request.user)
    if profile.role != 'company':
        return redirect('portal:dashboard')
    applications = Application.objects.filter(job__company=request.user).select_related('job', 'applicant', 'applicant__profile')
    status = request.GET.get('status', '')
    job_id = request.GET.get('job', '')
    if status:
        applications = applications.filter(status=status)
    if job_id:
        applications = applications.filter(job_id=job_id)
    return render(request, 'portal/company_applications.html', {
        'applications': applications,
        'jobs': Job.objects.filter(company=request.user),
        'status': status,
        'job_id': job_id,
        'status_choices': Application.STATUS_CHOICES,
    })


@login_required
def update_application_status(request, application_id):
    profile = get_profile(request.user)
    if profile.role != 'company':
        return redirect('portal:dashboard')
    application = get_object_or_404(Application, pk=application_id, job__company=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid = dict(Application.STATUS_CHOICES)
        if new_status in valid:
            application.status = new_status
            application.save(update_fields=['status', 'updated_at'])
            messages.success(request, 'Application status updated.')
    return redirect('portal:company_applications')


@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).select_related('job', 'job__company', 'job__company__profile')
    return render(request, 'portal/my_applications.html', {'applications': applications})


@login_required
def saved_jobs(request):
    saved = SavedJob.objects.filter(user=request.user).select_related('job', 'job__company', 'job__company__profile')
    return render(request, 'portal/saved_jobs.html', {'saved_jobs': saved})
