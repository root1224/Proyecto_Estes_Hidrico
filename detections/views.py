"""Detections views."""
# Django
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from django.shortcuts import redirect
from django_tables2 import SingleTableView
from django.views.generic.base import TemplateView
from django.shortcuts import render

# Tables
from detections.tables import NoteTable

# Forms
from detections.forms import DetectionForm

# Models
from detections.models import Detection, Note

# MyApps
from azucar.app import SaveFile, CalculateVi, SaveDetection


class IndexView(LoginRequiredMixin, ListView):
    """Return Index."""
    template_name = 'detections/index.html'
    model = Detection
    context_object_name = 'detetions'

class AllDetectionsView(LoginRequiredMixin, ListView):
    """Return detections."""
    template_name = 'detections/all.html'
    model = Detection
    ordering = ('-created',)
    paginate_by = 5
    context_object_name = 'detections'

class DetectionDetailView(LoginRequiredMixin, DetailView, SingleTableView):
    """Detection detail view."""
    template_name = 'detections/detail.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'
    model = Detection
    context_object_name = 'detection'

    def __init__(self, *args, **kwargs):
        super(DetectionDetailView, self).__init__(*args, **kwargs)
        self.object_list = self.get_queryset()

    def get_context_data(self, **kwargs):
        """Add detection's notes to context."""
        context = super().get_context_data(**kwargs)
        detection = self.get_object()
        context['notes'] = Note.objects.filter(note_detection=detection).order_by('-created')
        context['table'] = NoteTable(Note.objects.filter(note_detection=detection).order_by('-created'))
        return context


class LastDetectionView(LoginRequiredMixin, DetailView, SingleTableView):
    """Last detection view."""
    template_name = 'detections/detail.html'
    model = Detection
    context_object_name = 'detection'
    #table1 = NoteTable(Note.objects.filter(note_detection=Detection.objects.all().order_by('-created').first()))

    def __init__(self, *args, **kwargs):
        super(LastDetectionView, self).__init__(*args, **kwargs)
        self.object_list = self.get_queryset()

    def get_object(self, queryset=None):
        object_instance = Detection.objects.all().order_by('-created').first()
        return object_instance

    def get_context_data(self, **kwargs):
        """Add detection's notes to context."""
        context = super().get_context_data(**kwargs)
        detection = self.get_object()
        context['notes'] = Note.objects.filter(note_detection=detection).order_by('-created')
        context['table'] = NoteTable(Note.objects.filter(note_detection=Detection.objects.all().order_by('-created').first()))
        return context


class NewDetectionView(LoginRequiredMixin, TemplateView):
    """New detection view."""
    template_name = "detections/new.html"

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context

    def post(self, request, *args, **kwargs):
        if 'detect' in request.POST:
            for request_file in request.FILES.getlist('files'):
                SaveFile(request_file, request.user.username)

            CalculateVi(request.user.username)
            state='dead'
            context = {
                'save_detect' : True,
                'state': state
                }
            return render(request, self.template_name, context)

        elif 'save' in request.POST:
            user = request.user
            profile = request.user.profile
            detection_name = request.POST["name"]
            status = request.POST["satatus_of_field"]
            note_name = request.POST.getlist('note_name')
            note_text = request.POST.getlist('note_text')

            SaveDetection(request,user,profile,detection_name,status,note_name,note_text)
            return redirect('detections:last_detection')


        return render(request, self.template_name)
