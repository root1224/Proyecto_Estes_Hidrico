"""Main apps sugarcane."""

#Django
from django.core.files.storage import FileSystemStorage

# Others
import os
import rasterio

# Math libs
import numpy as np
import matplotlib.pyplot as plt  # Plot images


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
    return True
