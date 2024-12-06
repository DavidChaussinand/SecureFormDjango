from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send-test-email/', views.send_test_email, name='send_test_email'),
]
