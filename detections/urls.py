"""Detections URLs."""

# Django
from django.urls import path

# View
from detections import views

urlpatterns = [
        # Management
    path(
        route='',
        view=views.IndexView.as_view(),
        name='home'
    ),
    path(
        route='detections/',
        view=views.DetectionIndexView.as_view(),
        name='detections',
    ),
    #path('register/', register_user, name="register"),
    #path("logout/", LogoutView.as_view(), name="logout")
]
