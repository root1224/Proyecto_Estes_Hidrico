"""Main apps sugarcane."""

#Django
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

# Models
from detections.models import Detection, Note

# Others
import os
from io import StringIO, BytesIO
import rasterio
from django.core.files.base import ContentFile

# Math libs
import numpy as np
import matplotlib.pyplot as plt  # Plot images
from PIL import Image


def SaveFile(request_file, user):
    """Save bands images in temp file."""
    # https://docs.djangoproject.com/en/3.1/ref/files/storage/
    fs = FileSystemStorage()
    if 'RGB' in request_file.name:
        name = 'RGB_temp.JPG'
    elif 'NIR' in request_file.name:
        name = 'NIR_temp.TIF'
    elif 'RED' in request_file.name:
        name = 'RED_temp.TIF'
    else:
        name = 'Other_temp.JPG'

    path_folder_results = 'temp/results/' + str(user) + '/'
    path_folder = 'temp/bands/' + str(user) + '/'
    path_file =  path_folder + name

    if fs.exists(path_file):
        fs.delete(path_file)

    file = fs.save(path_file, request_file)  #request_file.name
    # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
    fileurl = fs.url(file)



def NDVI(RED, NIR):
    """Calculate NDVI"""
    # NDVI calculation
    ndvi=np.where(
        (NIR+RED)==0,
        0,
        (NIR-RED)/(NIR+RED)  # NDVI equation
    )
    vmin, vmax = np.nanpercentile(ndvi, (1,99))  # 1-99% contrast stretch
    return ndvi



def plot_vi(vi, N, color_map, vi_path):
    """Save or plot vegetation index image."""
    # Guardar imagen simple de indice de vegetacion
    plt.figure(figsize=(16.92,12.72), dpi=100)
    plt.imshow(vi, cmap=color_map)
    plt.axis("off")
    plt.savefig(vi_path, dpi=100, bbox_inches='tight', pad_inches=0)



def CalculateVi(user):
    """Calculate VIs."""
    # Paths
    path = os.getcwd()

    path_bands = path + '/media/temp/bands/' + str(user) + '/'
    path_resul = path + '/media/temp/results/' + str(user) + '/'

    red_path = path_bands + 'RED_temp.TIF'
    nir_path = path_bands + 'NIR_temp.TIF'

    path_ndvi_color = path_resul + 'NDVI.jpg'

    if not os.path.exists(path_resul):
        try:
            os.mkdir(path_resul)
        except OSError:
            print ("Creation of the directory %s failed" % path_resul)

    # Bands
    dsRED = rasterio.open(red_path)
    dsNIR = rasterio.open(nir_path)
    RED = dsRED.read(1).astype('float64')  # Red band from uint8 to float64
    NIR = dsNIR.read(1).astype('float64')  # Infrared band from uint8 to float64

    # Calculate VIs
    ndvi = NDVI(RED,NIR)

    # Values of plot_vi
    vi = ndvi               # Vegetation index
    n_clouster = None       # Clouster number
    color_map = 'RdYlGn'    # Color map

    # Export VI image
    plot_vi(
        vi = vi,
        N = n_clouster,
        color_map = color_map,
        vi_path = path_ndvi_color
    )


def SaveDetection(request,user,profile,detection_name,status,note_name,note_text):
    """Save detection in DB."""
    #https://stackoverflow.com/questions/35581356/save-matplotlib-plot-image-into-django-model/35633462
    #https://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
    path_picture = 'media/temp/bands/'+str(request.user.username)+'/RGB_temp.JPG'
    path_picture_ndvi ='media/temp/results/'+str(request.user.username)+'/NDVI.jpg'

    picture_name = 'RGB.jpg'
    picture_ndvi_name = 'NDVI.jpg'

    picture_file = Image.open(path_picture)
    picturer_ndvi_file = Image.open(path_picture_ndvi)

    tempfile_io = BytesIO()
    tempfile_ndvi_io = BytesIO()

    picture_file.save(tempfile_io, format='JPEG')
    picturer_ndvi_file.save(tempfile_ndvi_io, format='JPEG')

    picture_file = InMemoryUploadedFile(tempfile_io, None, picture_name,'image/jpeg',tempfile_io.tell, None)
    picture_ndvi_file = InMemoryUploadedFile(tempfile_ndvi_io, None, picture_ndvi_name,'image/jpeg',tempfile_ndvi_io.tell, None)

    detection_instance = Detection(
        user=user,
        profile=profile,
        name=detection_name,
        satatus_of_field=status,
        )
    detection_instance.picture.save(picture_name, picture_file)
    detection_instance.picture_ndvi.save(picture_ndvi_name, picture_ndvi_file)
    detection_instance.save()

    for n_name,n_text in zip(note_name,note_text):
        note_instance = Note(
            note_detection=detection_instance,
            name=n_name,
            user=user,
            text=n_text,
        )
        note_instance.save()

    return True
