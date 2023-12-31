# urls.py

from django.urls import path
from . import views 

app_name = 'calendar'
urlpatterns = [
    path('calendar/<int:year>/<int:month>/', views.monthly_calendar, name='monthly_calendar'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    # Add more URLs as needed
]
