"""Copy pets from local SQLite to the hosted Render API (one-time recovery)."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand

from main.models import Pet


class Command(BaseCommand):
    help = 'POST pets from this database to the live Render API (skips if remote already has pets).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            default='https://petpal-server-jbf4.onrender.com',
            help='Base URL of the deployed API (no trailing slash).',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Upload even when the remote API already returns pets.',
        )

    def handle(self, *args, **options):
        base = options['url'].rstrip('/')
        list_url = f'{base}/api/pet/'

        try:
            with urlopen(list_url, timeout=60) as response:
                remote = json.loads(response.read().decode())
        except (HTTPError, URLError) as err:
            self.stderr.write(self.style.ERROR(f'Could not reach {list_url}: {err}'))
            return

        if remote and not options['force']:
            self.stdout.write(
                self.style.WARNING(
                    f'Remote already has {len(remote)} pet(s). '
                    'Use --force to add copies anyway.'
                )
            )
            return

        pets = Pet.objects.all().order_by('id')
        if not pets.exists():
            self.stdout.write(self.style.WARNING('No pets in local database.'))
            return

        created = 0
        for pet in pets:
            body = json.dumps({
                'name': pet.name,
                'breed': pet.breed,
                'age': pet.age,
                'nickname': pet.nickname,
                'catchphrase': pet.catchphrase,
            }).encode()
            req = Request(
                f'{list_url}',
                data=body,
                headers={'Content-Type': 'application/json'},
                method='POST',
            )
            try:
                with urlopen(req, timeout=60) as response:
                    data = json.loads(response.read().decode())
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created {data.get('name', pet.name)} (id {data.get('id')})"))
            except HTTPError as err:
                detail = err.read().decode()
                self.stderr.write(self.style.ERROR(f"Failed for {pet.name}: {err.code} {detail}"))

        self.stdout.write(self.style.SUCCESS(f'Done. {created} pet(s) sent to {base}.'))
        self.stdout.write('Re-upload photos on each pet profile (photos are not copied by this command).')
