from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
