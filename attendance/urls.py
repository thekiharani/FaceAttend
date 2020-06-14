from django.urls import path
from .views import HomeView

app_name = 'attendance'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]