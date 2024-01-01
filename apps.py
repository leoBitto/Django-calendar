# calendar_app/apps.py

from django.apps import AppConfig

class CalendarAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calendar_app'

    def ready(self):
        
        import calendar_app.signals  # Importa il modulo dei segnali
