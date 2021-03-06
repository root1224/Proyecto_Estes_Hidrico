"""Create folders."""

#Django
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

# Others
import os
from PIL import Image


def ifExist(path_file, request_file):
    """Check if exists a folder."""
    # https://docs.djangoproject.com/en/3.1/ref/files/storage/
    fs = FileSystemStorage()
    if fs.exists(path_file):
        fs.delete(path_file)

    if request_file:
        file = fs.save(path_file, request_file)  #request_file.name
    # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
    # fileurl = fs.url(file)

def ifFolder(path):
    """Check if folder exists."""
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)


def rgb2gray(img,path,img_path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
    img = Image.open(img).convert('L')
    img.save(img_path)
