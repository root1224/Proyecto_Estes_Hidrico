"""Detections URLs."""

# Django
from django.urls import path

# View
from detections import views

urlpatterns = [
        # Management
    path(
        route='',
        view=views.DetectionIndexView.as_view(),
        name='home'
    ),
    #path('register/', register_user, name="register"),
    #path("logout/", LogoutView.as_view(), name="logout")
]
