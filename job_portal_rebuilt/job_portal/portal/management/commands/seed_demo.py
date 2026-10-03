from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the built-in demo companies and job listings.'

    def handle(self, *args, **options):
        call_command('migrate', verbosity=0)
        self.stdout.write(self.style.SUCCESS(
            'Demo marketplace is ready. Run the server and open http://127.0.0.1:8000/. '
            'Sample login password: Demo@12345'
        ))
