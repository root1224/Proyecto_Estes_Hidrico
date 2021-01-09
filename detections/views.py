"""Detections views."""
# Django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

# Models
from detections.models import Detection, Note


class IndexView(LoginRequiredMixin, ListView):
    """Return Index."""
    template_name = 'detections/index.html'
    model = Detection
    context_object_name = 'detetions'

class AllDetectionsView(LoginRequiredMixin, ListView):
    """Return detections."""
    template_name = 'detections/all-detections.html'
    model = Detection
    ordering = ('-created',)
    paginate_by = 5
    context_object_name = 'detections'

class DetectionDetailView(LoginRequiredMixin, DetailView):
    """Detection detail view."""
    template_name = 'detections/detail.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'
    queryset = Detection.objects.all()
    context_object_name = 'detection'

    def get_context_data(self, **kwargs):
        """Add detection's notes to context."""
        context = super().get_context_data(**kwargs)
        detection = self.get_object()
        context['notes'] = Note.objects.filter(note_detection=detection).order_by('-created')
        return context
