"""Detections views."""
# Django
from django.urls import reverse_lazy
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
from azucar.app import SaveFile, CalculateVi


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


class SaveDetectionView(LoginRequiredMixin, CreateView):
    """Save new detection."""
    template_name = 'detections/save.html'
    form_class = DetectionForm
    success_url = reverse_lazy('detections:last_detection')

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context



class NewDetectionView(LoginRequiredMixin, TemplateView):
    """New detection view."""
    template_name = "detections/new.html"

    def post(self, request, *args, **kwargs):
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')
        """
        for request_file in request.FILES.getlist('files'):
            SaveFile(request_file, request.user.username)

        if CalculateVi(request.user.username):
            """Success VI calculation."""
            template = reverse_lazy('detections:save_detection')
            return redirect(template)

        return render(request, self.template_name)


"""
class CreateDetectionView(LoginRequiredMixin):

    template_name = 'detections/new.html'
    model = Detection
    #form_class = DetectionForm
    #success_url = reverse_lazy('detections:last_detection')

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            if "detect" in request.POST:
                for file in request.FILES.getlist('files'):
                    img_save_path = "/media/temp/" + str(file)
                    with open(img_save_path, 'wb+') as f:
                        f.write(file.read())

        return super(CreateDetectionView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        Add user and profile to context.
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context
"""
