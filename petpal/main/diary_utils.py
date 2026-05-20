from datetime import date

from .models import Appointments, Daily, Health

DIARY_ENTRY_RELATIONS = {
    'daily': ('daily_logs', Daily),
    'vet_visit': ('health_records', Health),
    'appointment': ('appointments', Appointments),
}


def _field(label, value):
    if value is None or value == '':
        return None
    return {'label': label, 'value': str(value)}


def health_to_entry(record):
    fields = [
        _field('Date', record.date),
        _field('Visit type', record.visit_type),
        _field('Weight', record.pet_weight),
        _field('Shots', record.shots),
        _field('Medicines', record.meds),
        _field('Other notes', record.other),
        _field('Treatment plan', record.tx_plan),
        _field('Notes', record.notes),
    ]
    return {
        'id': record.id,
        'type': 'vet_visit',
        'label': 'Vet Visit',
        'fields': [f for f in fields if f],
    }


def daily_to_entry(record):
    log_labels = {
        'food': 'Feeding',
        'breakfast': 'Breakfast',
        'dinner': 'Dinner',
        'walk': 'Walk',
        'park': 'Park visit',
        'run': 'Ran around',
        'play_outside': 'Outdoor play',
        'swim': 'Swim',
        'hike': 'Hike / adventure',
        'yard': 'Yard or garden',
        'explore': 'Explored outside',
        'fetch': 'Played fetch',
        'train': 'Training session',
        'potty': 'Potty trip',
        'meds': 'Medication',
        'custom': 'Custom care',
        'general': 'Daily log',
    }
    label = log_labels.get(record.log_type, record.log_type.replace('_', ' ').title())
    fields = [
        _field('Date', record.date),
        _field('Details', record.details or record.daily_schedule),
        _field('Schedule', record.daily_schedule),
    ]
    return {
        'id': record.id,
        'type': 'daily',
        'label': label,
        'fields': [f for f in fields if f],
    }


def appointment_to_entry(record):
    fields = [
        _field('Date', record.date),
        _field('Title', record.title),
        _field('Details', record.description),
    ]
    return {
        'id': record.id,
        'type': 'appointment',
        'label': record.title or 'Appointment',
        'fields': [f for f in fields if f],
    }


def entry_date(record, fallback):
    if getattr(record, 'date', None):
        return record.date
    if getattr(record, 'appointment_date', None):
        return record.appointment_date.date()
    return fallback


def build_entries_by_date(pet, year, month):
    entries_by_date = {}
    month_start = date(year, month, 1)
    if month == 12:
        month_end = date(year + 1, 1, 1)
    else:
        month_end = date(year, month + 1, 1)

    def add(d, entry):
        if d is None:
            return
        key = d.isoformat()
        entries_by_date.setdefault(key, []).append(entry)

    for record in pet.health_records.filter(date__gte=month_start, date__lt=month_end):
        add(record.date, health_to_entry(record))

    for record in pet.daily_logs.filter(date__gte=month_start, date__lt=month_end):
        add(record.date, daily_to_entry(record))

    for record in pet.appointments.filter(date__gte=month_start, date__lt=month_end):
        add(record.date, appointment_to_entry(record))

    # Records without a date field fall back to created timestamp month
    for record in pet.health_records.filter(date__isnull=True):
        d = entry_date(record, None)
        if d and month_start <= d < month_end:
            add(d, health_to_entry(record))

    for record in pet.appointments.filter(date__isnull=True):
        d = entry_date(record, None)
        if d and month_start <= d < month_end:
            add(d, appointment_to_entry(record))

    return entries_by_date
