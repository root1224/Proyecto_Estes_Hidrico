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
        route='save-detection/',
        view=views.SaveDetectionView.as_view(),
        name='save_detection'
    ),
    path(
        route='new-detection/',
        view=views.NewDetectionView.as_view(),
        name='new_detection'
    ),
    path(
        route='detections/',
        view=views.AllDetectionsView.as_view(),
        name='all_detections',
    ),
    path(
        route='last_detection/',  # Detection Management
        view=views.LastDetectionView.as_view(),
        name='last_detection'
    ),
    path(
        route='<str:name>/',  # Detection Management
        view=views.DetectionDetailView.as_view(),
        name='detection_detail'
    ),

    #path("logout/", LogoutView.as_view(), name="logout")
]
