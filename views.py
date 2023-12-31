# views.py

import calendar as cal_module
from django.shortcuts import render, get_object_or_404
from .models import Event
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


def monthly_calendar(request, year, month):
    # Logica per ottenere il calendario del mese
    calendar_data = cal_module.monthcalendar(year, month)

    # Logica per ottenere gli eventi del mese
    #events = get_events_for_month(year, month)

    # Calcola il mese precedente
    selected_month = datetime(year, month, 1)
    prev_month = selected_month + relativedelta(months=-1)
    next_month = selected_month + relativedelta(months=+1)

    context = {
        'calendar': calendar_data,
        #'events': events,
        'year': year,
        'month': month,
        'prev_month': prev_month,
        'next_month': next_month,
    }


    return render(request, 'calendar/monthly_calendar.html',  context)


def get_events_for_month(year, month):
    # Logica per ottenere gli eventi del mese
    # Personalizza questa funzione in base alla tua logica di recupero degli eventi
    # Ad esempio, puoi utilizzare il tuo modello di evento e la query per ottenere gli eventi del mese
    start_date = date(year, month, 1)
    end_date = date(year, month + 1, 1) - timedelta(days=1)
    events = Event.objects.filter(start_date__range=[start_date, end_date])
    return events


def get_next_month(year, month):
    current_date = datetime(year, month, 1)
    next_month = current_date + timedelta(days=cal_module.monthrange(current_date.year, current_date.month)[1])
    return next_month.year, next_month.month

def get_previous_month(year, month):
    current_date = datetime(year, month, 1)
    first_day_of_month = datetime(current_date.year, current_date.month, 1)
    previous_month = first_day_of_month - timedelta(days=1)
    return previous_month.year, previous_month.month



def event_detail(request, event_id):
    # Retrieve the event using the event_id
    event = get_object_or_404(Event, id=event_id)

    context = {
        'event': event
        }


    return render(request, 'calendar/event_detail.html', context)
