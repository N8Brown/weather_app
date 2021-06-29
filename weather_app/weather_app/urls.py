from django.contrib import admin
from django.conf.urls import handler404
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('weather.urls', 'weather'), namespace='weather')),
]

handler404 = 'weather.views.error_404'