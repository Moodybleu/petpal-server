"""Copy pets from local SQLite to the hosted Render API (one-time recovery).

Requires your live login so pets are attached to your account. Example:

  python manage.py restore_pets_to_render \\
    --email meganbenn27@icloud.com \\
    --password 'your-live-password'
"""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand, CommandError

from main.models import Pet


def api_request(url, *, method='GET', data=None, token=None, timeout=60):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    body = json.dumps(data).encode() if data is not None else None
    req = Request(url, data=body, headers=headers, method=method)
    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode())


def fetch_token(base, login, password):
    login_url = f'{base}/api/user/login/'
    try:
        payload = api_request(
            login_url,
            method='POST',
            data={'email': login, 'password': password},
        )
    except HTTPError as err:
        detail = err.read().decode()
        raise CommandError(f'Login failed ({err.code}): {detail}') from err
    except URLError as err:
        raise CommandError(f'Could not reach {login_url}: {err}') from err

    token = payload.get('token')
    if not token:
        raise CommandError('Login response did not include a token.')
    return token


class Command(BaseCommand):
    help = 'POST pets from this database to the live Render API (requires login).'

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
        parser.add_argument(
            '--email',
            default=os.environ.get('PETPAL_RESTORE_EMAIL', ''),
            help='Live account email (or set PETPAL_RESTORE_EMAIL).',
        )
        parser.add_argument(
            '--password',
            default=os.environ.get('PETPAL_RESTORE_PASSWORD', ''),
            help='Live account password (or set PETPAL_RESTORE_PASSWORD).',
        )
        parser.add_argument(
            '--token',
            default=os.environ.get('PETPAL_RESTORE_TOKEN', ''),
            help='JWT from the live site (or set PETPAL_RESTORE_TOKEN).',
        )

    def handle(self, *args, **options):
        base = options['url'].rstrip('/')
        list_url = f'{base}/api/pet/'

        token = (options['token'] or '').strip()
        if not token:
            login = (options['email'] or '').strip()
            password = options['password'] or ''
            if not login or not password:
                raise CommandError(
                    'Provide --email and --password, --token, or set '
                    'PETPAL_RESTORE_EMAIL / PETPAL_RESTORE_PASSWORD / PETPAL_RESTORE_TOKEN.'
                )
            token = fetch_token(base, login, password)
            self.stdout.write('Logged in to live API.')

        try:
            remote = api_request(list_url, token=token)
        except (HTTPError, URLError) as err:
            raise CommandError(f'Could not list pets at {list_url}: {err}') from err

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
            body = {
                'name': pet.name,
                'breed': pet.breed,
                'age': pet.age,
                'nickname': pet.nickname,
                'catchphrase': pet.catchphrase,
            }
            try:
                data = api_request(list_url, method='POST', data=body, token=token)
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created {data.get('name', pet.name)} (id {data.get('id')})"
                    )
                )
            except HTTPError as err:
                detail = err.read().decode()
                self.stderr.write(
                    self.style.ERROR(f"Failed for {pet.name}: {err.code} {detail}")
                )

        self.stdout.write(self.style.SUCCESS(f'Done. {created} pet(s) sent to {base}.'))
        self.stdout.write(
            'Re-upload photos on each pet profile (photos are not copied by this command).'
        )
