from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # check from db
        from django_q.models import Schedule
        from .tasks import create_schedule_task

        task1 = Schedule.objects.filter(name='update_gold_price').exists()
        task2 = Schedule.objects.filter(name='publish_new_price').exists()
        if task1 and task2:
            return

        create_schedule_task()
