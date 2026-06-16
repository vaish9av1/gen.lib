import os
import sys

sys.path.append(r'c:\Vaish9av\Library Management System - Copy\library_system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

import django
django.setup()

from django.conf import settings

print('EMAIL_HOST:', settings.EMAIL_HOST)
print('EMAIL_PORT:', settings.EMAIL_PORT)
print('EMAIL_HOST_USER Set?', bool(settings.EMAIL_HOST_USER))
print('EMAIL_HOST_PASSWORD Set?', bool(settings.EMAIL_HOST_PASSWORD))
print('EMAIL_HOST_PASSWORD Length:', len(settings.EMAIL_HOST_PASSWORD))
