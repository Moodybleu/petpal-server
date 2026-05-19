import os
import secrets
from datetime import date

from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .auth_utils import create_access_token, get_user_id_from_request
from .diary_utils import build_entries_by_date
from .email_utils import (
    EmailDeliveryError,
    EmailNotConfiguredError,
    is_email_configured,
    send_login_reminder_email,
    send_password_reset_email,
)
from .models import Appointments, Daily, Health, Pet, User
from .pet_backup import DEFAULT_OWNER_EMAIL, PET_BACKUP
from .serializers import (
    AppointmentsSerializer,
    DailySerializer,
    HealthSerializer,
    PetSerializer,
    UserSerializer,
)


def home(request):
    return HttpResponse('Pet Pal Home Page')


EMAIL_NOT_CONFIGURED_MSG = (
    'Pet Pal cannot send email from the live server yet. '
    'Use the Reset password tab to choose a new password on this page instead, '
    'or ask the site owner to add RESEND_API_KEY or EMAIL_HOST on Render.'
)


def _send_user_email(send_callable, user):
    try:
        send_callable(user)
    except EmailNotConfiguredError:
        return Response(
            {'msg': EMAIL_NOT_CONFIGURED_MSG},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except EmailDeliveryError:
        return Response(
            {'msg': 'Could not send email. Check your address and try again later.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception:
        return Response(
            {'msg': 'Could not send email. Try again later.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return None


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = create_access_token(user.id)
        return Response(
            {'token': token, 'user': UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        login_id = (
            request.data.get('login', '').strip()
            or request.data.get('username', '').strip()
            or request.data.get('email', '').strip()
        )
        password = request.data.get('password', '').strip()

        if not login_id or not password:
            return Response(
                {'msg': 'Username or email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if '@' in login_id:
            user = User.objects.filter(email__iexact=login_id).first()
        else:
            user = User.objects.filter(name__iexact=login_id).first()

        if not user:
            return Response(
                {'msg': 'Invalid username or password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not check_password(password, user.password):
            return Response(
                {'msg': 'Invalid username or password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = create_access_token(user.id)
        return Response({'token': token})

    @action(detail=False, methods=['post'], url_path='remind-login')
    def remind_login(self, request):
        email = request.data.get('email', '').strip()
        if not email:
            return Response(
                {'msg': 'Please enter the email you used when you signed up.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email__iexact=email).first()
        success_msg = (
            'If that email is registered with Pet Pal, we sent your login details. '
            'Check your inbox (and spam folder).'
        )

        if user:
            if not is_email_configured():
                return Response(
                    {'msg': EMAIL_NOT_CONFIGURED_MSG},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            temporary_password = secrets.token_urlsafe(9)
            email_error = _send_user_email(
                lambda u: send_login_reminder_email(u, temporary_password),
                user,
            )
            if email_error:
                return email_error
            user.password = make_password(temporary_password)
            user.save(update_fields=['password'])

        return Response({'msg': success_msg})

    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        email = request.data.get('email', '').strip()
        new_password = request.data.get('new_password', '')
        confirm_password = request.data.get('confirm_password', '')

        if not email:
            return Response(
                {'msg': 'Please enter the email you used when you signed up.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not new_password:
            return Response(
                {'msg': 'Please enter a new password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if new_password != confirm_password:
            return Response(
                {'msg': 'Passwords do not match.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(new_password) < 6:
            return Response(
                {'msg': 'Password must be at least 6 characters.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response(
                {
                    'msg': (
                        'No account found with that email. '
                        'Sign up first, then log in or reset your password.'
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        user.password = make_password(new_password)
        user.save(update_fields=['password'])
        if is_email_configured():
            _send_user_email(send_password_reset_email, user)

        return Response({
            'msg': 'Password updated. Log in with your new password below.',
        })

    @action(detail=False, methods=['post'], url_path='seed-pets-if-empty')
    def seed_pets_if_empty(self, request):
        """One-time recovery when Render wipes SQLite (only if no pets exist yet)."""
        if Pet.objects.exists():
            return Response(
                {'msg': 'Pets already exist; seed skipped.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        owner_email = os.environ.get('PETPAL_OWNER_EMAIL', DEFAULT_OWNER_EMAIL).strip()
        owner = User.objects.filter(email__iexact=owner_email).first()
        if not owner:
            return Response(
                {
                    'msg': (
                        f'No account for {owner_email} yet. '
                        'Sign up on the live site, then try again.'
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        created = []
        for data in PET_BACKUP:
            pet = Pet.objects.create(owner=owner, **data)
            created.append({'id': pet.id, 'name': pet.name})

        return Response({'msg': f'Restored {len(created)} pet(s).', 'pets': created})


class PetView(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        user_id = get_user_id_from_request(self.request)
        if not user_id:
            return Pet.objects.none()
        return Pet.objects.filter(owner_id=user_id)

    def perform_create(self, serializer):
        user_id = get_user_id_from_request(self.request)
        if not user_id:
            raise PermissionDenied('Login required to add a pet.')
        serializer.save(owner_id=user_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['get'], url_path='diary')
    def diary(self, request, pk=None):
        pet = self.get_object()
        today = date.today()
        year = int(request.query_params.get('year', today.year))
        month = int(request.query_params.get('month', today.month))

        if month < 1 or month > 12:
            return Response({'detail': 'Month must be between 1 and 12.'}, status=status.HTTP_400_BAD_REQUEST)

        entries_by_date = build_entries_by_date(pet, year, month)

        return Response({
            'pet': PetSerializer(pet).data,
            'year': year,
            'month': month,
            'entries_by_date': entries_by_date,
        })


class PetFilteredViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        pet_id = self.request.query_params.get('pet')
        if pet_id:
            queryset = queryset.filter(pet_id=pet_id)
        return queryset


class HealthView(PetFilteredViewSet):
    serializer_class = HealthSerializer
    queryset = Health.objects.all()


class DailyView(PetFilteredViewSet):
    serializer_class = DailySerializer
    queryset = Daily.objects.all()


class AppointmentsView(PetFilteredViewSet):
    serializer_class = AppointmentsSerializer
    queryset = Appointments.objects.all()
