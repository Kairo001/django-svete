"""Modelo que será la base para el resto de modelos del proyecto."""

# Django
from django.db import models

class BaseModel(models.Model):
    """Modelo base.
    Actúa como una clase base abstracta de la que heredarán todos los demás modelos del projecto.
    Esta clase proporciona a cada tabla los siguientes atributos:

        + created(DateTime): Almacena la fecha y la hora en la cual se creó la instancia.
        + modified(DateTime): Almacena la fecha y la hora de la última modificación de cada instancia.
    """

    created = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación de la instancia.")
    modified = models.DateTimeField(auto_now=True, help_text="Fecha y hora de la última modificación de la instancia.")

    class Meta:
        """Opciones meta para BaseModel."""
        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']
