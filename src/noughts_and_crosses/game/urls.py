from django.urls import path, include
from django.views.generic import TemplateView, ListView
from rest_framework.views import APIView

from . import views

# urlpatterns = [
#     path('', APIView.as_view(), name='index'),
# ]