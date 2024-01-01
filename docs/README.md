# Calendar App Documentation

## Introduction

Welcome to the documentation for the Calendar app! This app is designed to manage events and link them to custom models with a "date" field. The documentation will cover installation, configuration, and basic usage of the app.

## Installation

To get started, make sure you have Django installed in your project. You can install the Calendar app using pip:

```bash
pip install django-calendar
```

Add 'calendar_app' to your installed apps in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'calendar_app',
    # ...
]
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Configuration

### Signals

Signals are used to automatically create `EventLink` instances when a linked object is created or deleted, when a linked object is deleted the event is deeted as well:

```python
# In the signals.py file
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from .models import EventLink

@receiver(post_save)
def create_event_link(sender, instance, created, **kwargs):
    if created and has_date_field(instance):
        # Create an EventLink instance associated with the object
        EventLink.objects.create(
            object_date=get_date_field_value(instance),
            content_type=ContentType.objects.get_for_model(sender),
            object_id=instance.id,
        )

@receiver(pre_delete)
def delete_event_link(sender, instance, **kwargs):
    try:
        # Try to get the value of the 'object_date' field
        object_date = getattr(instance, 'date', None)

        if object_date:
            # Find and delete the EventLink associated with the object about to be deleted
            content_type = ContentType.objects.get_for_model(sender)
            event_link = EventLink.objects.filter(
                content_type=content_type,
                object_id=instance.id,
                object_date=object_date
            ).first()

            if event_link:
                event_link.delete()
    except Exception as e:
        # Handle any exceptions during execution
        pass

def has_date_field(instance):
    # Check if the object has a 'date' field (add other fields if necessary)
    return hasattr(instance, 'date')

def get_date_field_value(instance):
    # Get the value of the 'date' field (add other fields if necessary)
    return getattr(instance, 'date', None)
```

# In the apps.py file
``` python

# Add the signal to the `apps.py` file:
from django.apps import AppConfig

class CalendarAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calendar_app'

    def ready(self):
        import calendar_app.signals  # Import the signals module
```

## Using the App

### Managing Events

Events are managed through the `EventLink` model. You can get events for a specific month using the `get_events_for_month` function in the `views.py` file:

```python
# In the views.py file
import calendar as cal_module
from django.shortcuts import render
from .models import EventLink
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def monthly_calendar(request, year, month):
    # Logic to get the month's calendar
    calendar_data = cal_module.monthcalendar(year, month)

    # Logic to get the month's events
    events = get_events_for_month(year, month)

    # Calculate the previous and next month
    prev_month = get_previous_month(year, month)
    next_month = get_next_month(year, month)

    context = {
        'calendar': calendar_data,
        'events': events,
        'year': year,
        'month': month,
        'prev_month': prev_month,
        'next_month': next_month,
    }

    return render(request, 'calendar/monthly_calendar.html', context)

def get_events_for_month(year, month):
    # Calculate the start and end date of the month
    start_date = date(year, month, 1)
    _, last_day = cal_module.monthrange(year, month)
    end_date = start_date + relativedelta(day=last_day)

    # Filter for events that have the date equal to the selected month
    events = EventLink.objects.filter(
        object_date__gte=start_date,
        object_date__lte=end_date
    )

    return events

def get_next_month(year, month):
    current_date = datetime(year, month, 1)
    next_month = current_date + relativedelta(months=+1)
    return next_month.year, next_month.month

def get_previous_month(year, month):
    current_date = datetime(year, month, 1)
    previous_month = current_date - relativedelta(months=1)
    return previous_month.year, previous_month.month

def event_detail(request, event_id):
    # Retrieve the event using the event_id
    event = get_object_or_404(Event, id=event_id)

    context = {
        'event': event
    }

    return render(request, 'calendar/event_detail.html', context)
```

**Note:** Insert the signals (`signals.py`) and the app (`apps.py`) in the correct files of your app, as shown above. Make sure the functions are called correctly in the `signals.py` and `apps.py` files.

This should cover the configuration and usage of the Calendar app in your Django project. If you have further questions or need additional clarification, feel free to ask!