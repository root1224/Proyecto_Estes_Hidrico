""" Detections models."""
# Django
# https://github.com/django/django/blob/master/django/contrib/auth/models.py
from django.db import models # https://docs.djangoproject.com/en/3.1/ref/models/fields/
from django.contrib.auth.models import User



class Detection(models.Model):
    """ Profile model.
    Proxy model that extends the base data with other
    information.
    """
    DEAD = 'dead'
    SAVE = 'save'
    GOOD = 'good'

    SATATUS_OF_FIELD = [
        (DEAD, 'Dead'),
        (SAVE, 'Save'),
        (GOOD, 'Good'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=20)
    picture = models.ImageField(
        upload_to='detections/RGB',
    )

    picture_ndvi = models.ImageField(
        upload_to='detections/NDVI'
    )
    picture_savi = models.ImageField(
        upload_to='detections/SAVI'
    )
    picture_evi2 = models.ImageField(
        upload_to='detections/EVI2'
    )


    satatus_of_field = models.CharField(
        max_length=10,
        choices=SATATUS_OF_FIELD,
        default=GOOD,
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ Return detection name. """
        return self.name


class Note(models.Model):
    """ Note model."""
    note_detection = models.ForeignKey(Detection,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    #def get_notes(self):
    #    return "\n".join([note.name for note in self.notes.all()])
