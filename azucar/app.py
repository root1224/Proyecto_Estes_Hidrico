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
from rasterio.plot import reshape_as_raster, reshape_as_image
from django.core.files.base import ContentFile

# Math libs
import numpy as np
import matplotlib.pyplot as plt  # Plot images
from PIL import Image

# My apps
from .clous import cloustering
from .VI import Calulate_VIS
from .folders import ifFolder, rgb2gray
from .SaveFiles import SaveVI


def CalculateVi(user):
    """Calculate VIs."""
    # Paths
    path = os.getcwd()
    path_bands = path + '/media/temp/bands/' + str(user) + '/'
    path_resul = path + '/media/temp/results/' + str(user) + '/'
    ifFolder(path_resul)

    # Bands paths
    red_path = path_bands + 'RED_temp.TIF'
    nir_path = path_bands + 'NIR_temp.TIF'

    # Vi paths
    path_ndvi = path_resul + 'NDVI.jpg'
    path_savi = path_resul + 'SAVI.jpg'
    path_evi2 = path_resul + 'EVI2.jpg'

    # Bands
    dsRED = rasterio.open(red_path)
    dsNIR = rasterio.open(nir_path)
    RED = dsRED.read(1).astype('float64')  # Red band from uint8 to float64
    NIR = dsNIR.read(1).astype('float64')  # Infrared band from uint8 to float64

    # Calculate VIs
    ndvi,savi,evi2 = Calulate_VIS(RED,NIR)

    path_vis = [path_ndvi,path_savi,path_evi2]
    vis = [ndvi,savi,evi2]

    # Export VI image
    for vi,path in zip(vis,path_vis):
        SaveVI(
            vi=vi,
            vi_path=path
        )

def MakeCloustering(user,number,path_detection):
    """Make cloustering."""
    # Paths
    path = os.getcwd()
    path_clouster = path + '/media/temp/clouster/' + str(user) + '/'
    clouster_vi = path_clouster + 'clouster_done.jpg'

    picture_path = path + '/media' + path_detection

    # Values of plot_vi
    rgb2gray(picture_path,path_clouster,clouster_vi) # Img a convertir, path en donde se guarda

    vi = rasterio.open(clouster_vi).read()  # Vegetation index
    n_clouster = number       # Clouster number

    # Export VI image
    SaveVI(
        vi = reshape_as_image(vi),
        N = n_clouster,
        vi_path = clouster_vi
    )
