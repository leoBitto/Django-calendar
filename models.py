# calendar_app/models.py

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class EventLink(models.Model):
    object_date = models.DateField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Altri campi che potresti voler aggiungere

    def __str__(self):
        return f"{self.content_object} - {self.object_date}"
    

@receiver(pre_delete)
def delete_event_link(sender, instance, **kwargs):
    try:
        # Prova a ottenere il valore del campo 'object_date'
        object_date = getattr(instance, 'date', None)

        if object_date:
            # Trova e cancella l'EventLink associato all'oggetto che sta per essere eliminato
            content_type = ContentType.objects.get_for_model(sender)
            event_link = EventLink.objects.filter(
                content_type=content_type,
                object_id=instance.id,
                object_date=object_date
            ).first()

            if event_link:
                event_link.delete()
    except Exception as e:
        # Gestisci eventuali eccezioni durante l'esecuzione
        pass
