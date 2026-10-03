from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('companies/', views.company_directory, name='company_directory'),
    path('job-alerts/', views.job_alerts, name='job_alerts'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('jobs/<int:job_id>/save/', views.toggle_save_job, name='toggle_save_job'),
    path('company/jobs/new/', views.create_job, name='create_job'),
    path('company/jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('company/jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('company/applications/', views.company_applications, name='company_applications'),
    path('company/applications/<int:application_id>/status/', views.update_application_status, name='update_application_status'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('saved-jobs/', views.saved_jobs, name='saved_jobs'),
]
