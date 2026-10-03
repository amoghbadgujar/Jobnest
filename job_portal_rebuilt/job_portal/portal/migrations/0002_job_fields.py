from django.db import migrations, models


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


class Migration(migrations.Migration):
    dependencies = [('portal', '0001_initial')]
    operations = [
        migrations.AddField(
            model_name='job', name='category',
            field=models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='technology'),
        ),
        migrations.AddField(
            model_name='job', name='is_featured', field=models.BooleanField(default=False),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['category'], name='portal_job_category_idx'),
        ),
    ]
