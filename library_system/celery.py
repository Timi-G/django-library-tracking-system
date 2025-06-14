import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

app = Celery('library_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Please note that django_celery_beat was used so scheduling can be managed in Django Admin Panel 
# A periodic task check_overdue_loans has been created in Admin Panel

@app.task(bind=True, ignore_results=True)
def debug_task(self):
    print(f"Request: {self.request!r}")