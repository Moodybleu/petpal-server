"""Re-create backed-up pets on startup when the hosted DB was wiped."""

import os

from django.core.management.base import BaseCommand

from main.models import Pet, User
from main.pet_backup import DEFAULT_OWNER_EMAIL, PET_BACKUP


class Command(BaseCommand):
    help = 'Create backed-up pets for the owner account when they have none (Render recovery).'

    def handle(self, *args, **options):
        owner_email = os.environ.get('PETPAL_OWNER_EMAIL', DEFAULT_OWNER_EMAIL).strip()
        owner = User.objects.filter(email__iexact=owner_email).first()
        if not owner:
            self.stdout.write(
                self.style.WARNING(
                    f'No user with email {owner_email!r} yet — skip pet seed until they sign up.'
                )
            )
            return

        existing = Pet.objects.filter(owner=owner).count()
        if existing:
            self.stdout.write(f'Owner already has {existing} pet(s); nothing to seed.')
            return

        created = 0
        for data in PET_BACKUP:
            Pet.objects.create(owner=owner, **data)
            created += 1
            self.stdout.write(self.style.SUCCESS(f"Seeded {data['name']} for {owner_email}"))

        self.stdout.write(self.style.SUCCESS(f'Done. {created} pet(s) created.'))
