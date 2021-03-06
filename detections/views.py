"""Detections views."""
# Django
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from django.shortcuts import redirect
from django_tables2 import SingleTableView
from django.views.generic.base import TemplateView
from django.shortcuts import render


# Forms
from detections.forms import DetectionForm

# Models
from detections.models import Detection, Note

# MyApps
from azucar.app import CalculateVi, MakeCloustering
from azucar.SaveFiles import SaveFile,SaveDetection


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
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if 'cloustering_ndvi' in request.POST:
            detection = self.get_object()
            if int(request.POST['n_clouster_ndvi']) != 0:
                number = request.POST['n_clouster_ndvi']
                type_vi = 'ndvi'
                picture_url = detection.picture_ndvi.url

                MakeCloustering(request.user,int(number),picture_url)
                context['done_clouster'] = type_vi

        elif 'cloustering_savi' in request.POST:
            detection = self.get_object()
            if int(request.POST['n_clouster_savi']) != 0:
                number = request.POST['n_clouster_savi']
                type_vi = 'savi'
                picture_url = detection.picture_savi.url

                MakeCloustering(request.user,int(number),picture_url)
                context['done_clouster'] = type_vi

        elif 'cloustering_evi2' in request.POST:
            detection = self.get_object()
            if int(request.POST['n_clouster_evi2']) != 0:
                number = request.POST['n_clouster_evi2']
                type_vi = 'evi2'
                picture_url = detection.picture_evi2.url

                MakeCloustering(request.user,int(number),picture_url)
                context['done_clouster'] = type_vi

        elif 'delete' in request.POST:
            id = request.POST['id_note']
            note_instance= Note.objects.get(id=id)
            note_instance.delete()

        return render(request, 'detections/detail.html', context)


class LastDetectionView(LoginRequiredMixin, DetailView, SingleTableView):
    """Last detection view."""
    template_name = 'detections/detail.html'
    model = Detection
    context_object_name = 'detection'

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
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if 'cloustering_ndvi' in request.POST:
            detection = self.get_object()
            if int(request.POST['n_clouster']) != 0:
                number = request.POST['n_clouster']
                type_vi = 'ndvi'
                picture_url = detection.picture_ndvi.url

                MakeCloustering(request.user,int(number),picture_url)
                context['done_clouster'] = type_vi

        elif 'cloustering_savi' in request.POST:
            detection = self.get_object()
            if int(request.POST['n_clouster']) != 0:
                number = request.POST['n_clouster']
                type_vi = 'savi'
                picture_url = detection.picture_savi.url

                MakeCloustering(request.user,int(number),picture_url)
                context['done_clouster'] = type_vi

        elif 'cloustering_evi2' in request.POST:
            detection = self.get_object()
            if int(request.POST['n_clouster']) != 0:
                number = request.POST['n_clouster']
                type_vi = 'evi2'
                picture_url = detection.picture_evi2.url

                MakeCloustering(request.user,int(number),picture_url)
                context['done_clouster'] = type_vi

        elif 'delete' in request.POST:
            id = request.POST['id_note']
            note_instance= Note.objects.get(id=id)
            note_instance.delete()

        return render(request, 'detections/detail.html', context)


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
            files_detection = request.FILES.getlist('files')
            if files_detection:
                if len(files_detection) == 3:
                    extention = []
                    if not any("RGB" in s.name for s in files_detection):
                        extention.append("RGB")
                    if not any("NIR" in s.name for s in files_detection):
                        extention.append("NIR")
                    if not any("RED" in s.name for s in files_detection):
                        extention.append("RED")

                    if not extention:
                        for request_file in files_detection:
                            SaveFile(request_file, request.user.username)

                        CalculateVi(request.user.username)
                        state='dead'
                        context = {
                            'save_detect' : True,
                            'state': state
                            }
                    else:
                        context = { 'msg' : 'Select files: '+','.join([str(n) for n in extention]) }

                else:
                    context = {
                        'msg' : 'Select three files.'
                    }

            else:
                context = {
                    'msg' : 'Select files.'
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
