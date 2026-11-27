import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isbms.settings')

application = get_wsgi_application()

# Ensure pending migrations (e.g. on cloud platforms whose build command skips migrate) are applied on startup.
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False, verbosity=0)
except Exception as exc:
    print(f"[VyaparSetu WSGI] Auto-migrate note: {exc}")

app = application
