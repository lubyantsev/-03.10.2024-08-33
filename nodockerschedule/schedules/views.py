from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Schedule, Event
from .forms import ScheduleForm, EventForm, PasswordForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def home_view(request):
    schedules = Schedule.objects.all()
    event_form = EventForm()

    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            schedule_id = request.POST.get('schedule_id')
            schedule = Schedule.objects.get(id=schedule_id)
            event.schedule = schedule
            event.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'schedule_{schedule.id}',
                {
                    'type': 'new_event',
                    'event': {
                        'time': event.time.isoformat(),
                        'place': event.place,
                        'participant_name': event.participant_name,
                    }
                }
            )
            return redirect('home')

    return render(request, 'schedules/home.html', {
        'event_form': event_form,
        'schedules': schedules,
    })


def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Расписание успешно создано!')
            return redirect('home')
    else:
        form = ScheduleForm()
    return render(request, 'schedules/create_schedule.html', {'form': form})


def schedule_detail_view(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    events = Event.objects.filter(schedule=schedule)

    if request.method == 'POST':
        password_form = PasswordForm(request.POST)
        if password_form.is_valid() and password_form.cleaned_data['password'] == schedule.password:
            return render(request, 'schedules/schedule_detail.html', {
                'schedule': schedule,
                'events': events,
            })
        else:
            messages.error(request, 'Неверный пароль.')

    password_form = PasswordForm()
    return render(request, 'schedules/schedule_detail.html', {
        'schedule': schedule,
        'events': events,
        'password_form': password_form,
    })