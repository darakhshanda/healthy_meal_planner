from django.apps import AppConfig


class MealappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mealapp'


def ready(self):
    import mealapp.signals
