from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_create_missing_profiles'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('keyword', models.CharField(blank=True, max_length=120)),
                ('location', models.CharField(blank=True, max_length=120)),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly')], default='weekly', max_length=10)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='jobalert',
            constraint=models.UniqueConstraint(fields=('email', 'keyword', 'location'), name='unique_job_alert'),
        ),
    ]
