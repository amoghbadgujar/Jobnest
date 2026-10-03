from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Application, Job, JobAlert, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=60, required=True)
    last_name = forms.CharField(max_length=60, required=False)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, widget=forms.RadioSelect)
    company_name = forms.CharField(max_length=160, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get('role')
        company_name = cleaned.get('company_name', '').strip()
        if role == 'company' and not company_name:
            self.add_error('company_name', 'Company name is required for company accounts.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'role': self.cleaned_data['role'],
                    'company_name': self.cleaned_data.get('company_name', '').strip(),
                },
            )
        return user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=60, required=True)
    last_name = forms.CharField(max_length=60, required=False)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = [
            'phone', 'location', 'headline', 'bio', 'company_name',
            'company_website', 'resume', 'avatar'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def clean_company_name(self):
        value = self.cleaned_data.get('company_name', '').strip()
        if self.instance.role == 'company' and not value:
            raise forms.ValidationError('Company name is required.')
        return value

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data.get('last_name', '')
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'category', 'description', 'requirements', 'location', 'job_type',
            'work_mode', 'experience', 'skills', 'salary_min', 'salary_max',
            'openings', 'deadline', 'is_active', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'requirements': forms.Textarea(attrs={'rows': 6}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        minimum = cleaned.get('salary_min') or 0
        maximum = cleaned.get('salary_max') or 0
        if maximum and minimum and maximum < minimum:
            raise forms.ValidationError('Maximum salary cannot be lower than minimum salary.')
        return cleaned


class JobAlertForm(forms.ModelForm):
    class Meta:
        model = JobAlert
        fields = ['email', 'keyword', 'location', 'frequency']
        widgets = {
            'keyword': forms.TextInput(attrs={'placeholder': 'Python, UX, product manager'}),
            'location': forms.TextInput(attrs={'placeholder': 'Pune, Remote, India'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
        }

    def clean(self):
        cleaned = super().clean()
        keyword = (cleaned.get('keyword') or '').strip()
        location = (cleaned.get('location') or '').strip()
        if not keyword and not location:
            raise forms.ValidationError('Add at least one keyword or location to receive relevant alerts.')
        return cleaned


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {'cover_letter': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Tell the employer why you are a good fit...'})}
