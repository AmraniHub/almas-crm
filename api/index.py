import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almas_crm.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Run migrations once on cold start — only if DB is reachable
try:
    from django.core.management import call_command
    from django.db import connection
    connection.ensure_connection()
    call_command('migrate', '--run-syncdb', verbosity=0)

    # Create admin user from environment variables (never hardcoded)
    from django.contrib.auth.models import User
    admin_user = os.environ.get('ADMIN_USER', 'almas')
    admin_pass = os.environ.get('ADMIN_PASS', '')
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@almas.ma')

    if admin_pass and not User.objects.filter(username=admin_user).exists():
        User.objects.create_superuser(admin_user, admin_email, admin_pass)
except Exception:
    pass

app = application
