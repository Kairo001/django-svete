"""Modelos de la app core."""

# Django
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Utilidades
from utils.models import BaseModel

class UserManager(BaseUserManager):
    """Administrador del modelo de usuarios para crear los diferentes roles."""

    def _create_user(self, first_name, last_name, email, password, is_staff, is_superuser, **extra_fields):

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        return self._create_user(first_name, last_name, email, password, False, False, **extra_fields)

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        return self._create_user(first_name, last_name, email, password, True, True, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado."""
    first_name = models.CharField('Nombres', max_length=32)
    last_name = models.CharField('Apellidos', max_length=32)
    email = models.EmailField(
        'Correo electrónico', 
        max_length=32,
        unique=True        
    )

    is_staff = models.BooleanField(
        default=False,
        help_text='Designa si el usuario puede iniciar sesión en el sitio de administración.',
    )

    is_active = models.BooleanField(
        default=True,
        help_text=(
            'Designa si este usuario debe ser tratado como activo.'
            'Desmarcar esto en lugar de eliminar usuarios.'
        ),
    )

    objects: UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    EMAIL_FIELD = 'email'

    class Meta:
        """Opciones meta para User."""
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.first_name + self.last_name

class UserToken(BaseModel):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    expired_at = models.DateTimeField()

    def __str__(self):
        return 'Token del usuario con id {}.'.format(self.user_id)

class Reset(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.email