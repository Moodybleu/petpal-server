from django.db import migrations


def dedupe_user_emails(apps, schema_editor):
    User = apps.get_model('main', 'User')
    seen = set()
    for user in User.objects.order_by('id'):
        key = (user.email or '').strip().lower()
        if not key:
            continue
        if key in seen:
            user.delete()
        else:
            seen.add(key)


class Migration(migrations.Migration):
    # PostgreSQL cannot ALTER the same table in the same transaction as row deletes.
    atomic = False

    dependencies = [
        ('main', '0008_user_password_length'),
    ]

    operations = [
        migrations.RunPython(dedupe_user_emails, migrations.RunPython.noop),
    ]
