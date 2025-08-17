# import os
# from celery import Celery
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')
#
# app = Celery('university_portal')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()




# proj/proj/celery.py
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')

app = Celery('university_portal')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')