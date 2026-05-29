import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almas_crm.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Run migrations and create default admin on cold start
try:
    from django.core.management import call_command
    call_command('migrate', '--run-syncdb', verbosity=0)

    from django.contrib.auth.models import User
    if not User.objects.filter(username='almas').exists():
        User.objects.create_superuser('almas', 'admin@almas.ma', 'Almas2024!')
except Exception:
    pass

app = application
