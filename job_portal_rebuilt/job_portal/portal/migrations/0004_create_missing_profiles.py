from django.db import migrations


def create_missing_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('portal', 'Profile')
    for user in User.objects.filter(profile__isnull=True):
        Profile.objects.create(user=user)


class Migration(migrations.Migration):
    dependencies = [('portal', '0003_seed_jobs')]

    operations = [migrations.RunPython(create_missing_profiles, migrations.RunPython.noop)]
