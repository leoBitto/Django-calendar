# calendar_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from .models import EventLink
from django.contrib.contenttypes.models import ContentType

@receiver(post_save)
def create_event_link(sender, instance, created, **kwargs):
    if created and has_date_field(instance):
        # Crea un'istanza di EventLink associata all'oggetto
        EventLink.objects.create(
            object_date=get_date_field_value(instance),
            content_type=ContentType.objects.get_for_model(sender),
            object_id=instance.id,
        )

def has_date_field(instance):
    # Verifica se l'oggetto ha un campo 'date' (aggiungi altri campi se necessario)
    return hasattr(instance, 'date')

def get_date_field_value(instance):
    # Ottieni il valore del campo 'date' (aggiungi altri campi se necessario)
    return getattr(instance, 'date', None)
