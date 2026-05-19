from datetime import date

from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .auth_utils import create_access_token, get_user_id_from_request
from .diary_utils import build_entries_by_date
from .models import Appointments, Daily, Health, Pet, User
from .serializers import (
    AppointmentsSerializer,
    DailySerializer,
    HealthSerializer,
    PetSerializer,
    UserSerializer,
)


def home(request):
    return HttpResponse('Pet Pal Home Page')


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
        password = request.data.get('password', '')

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
