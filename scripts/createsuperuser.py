import os, sys

os.chdir('..')
project_path = os.getcwd()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "S2G4RealEstate.settings")
sys.path.append(project_path)

os.chdir(project_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth.models import User
try:
    User.objects.create_superuser(username='admin', password='12345', email='admin@test.com')
except:
    pass
    
print('Super User Created: {}'.format(User.objects.get(username='admin')) )
