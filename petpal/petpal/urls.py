from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve as media_serve
from rest_framework import routers

from main import views

router = routers.DefaultRouter()
router.register(r'user', views.UserView, 'user')
router.register(r'pet', views.PetView, 'pet')
router.register(r'health', views.HealthView, 'health')
router.register(r'daily', views.DailyView, 'daily')
router.register(r'appointments', views.AppointmentsView, 'appointments')

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('user/', include(router.urls)),
]

# static() only registers media routes when DEBUG=True; serve explicitly for production.
urlpatterns += [
    re_path(
        r'^media/(?P<path>.*)$',
        media_serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
