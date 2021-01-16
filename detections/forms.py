"""Detection forms."""

# Django
from django import forms

# Models
from detections.models import Detection, Note


class DetectionForm(forms.ModelForm):
    """Detection model form."""

    class Meta:
        """Form settings."""
        model = Detection
        fields = ('user', 'name', 'picture', 'picture_ndvi', 'satatus_of_field')
