import os
import django

django.setup()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chattey.settings')

application = get_wsgi_application()
