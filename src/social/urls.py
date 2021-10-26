from django.urls import path
from .views import GoogleView

urlpatterns = [
    path('google/', GoogleView.as_view(), name='google'),
]
