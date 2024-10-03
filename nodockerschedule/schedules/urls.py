from django.urls import path
from .views import home_view, create_schedule, schedule_detail_view
from . import consumers

websocket_urlpatterns = [
    path('ws/schedule/<int:schedule_id>/', consumers.ScheduleConsumer.as_asgi()),
]

urlpatterns = [
    path('', home_view, name='home'),
    path('create_schedule/', create_schedule, name='create_schedule'),
    path('schedule/<int:schedule_id>/', schedule_detail_view, name='schedule_detail'),
]