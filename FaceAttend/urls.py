
from django.contrib import admin
from django.urls import path, include
from accounts.views import login_success

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance.urls', namespace='attendance')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login_success/', login_success, name='login_success')
]
