"""Vistas para la app core."""

# Django
from django.core.mail import send_mail

# RestFramework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions

# Serializadores
from core.serializers import UserSerializer

# Modelos
from core.models import Reset, User, UserToken

# Access & refresh token
from core.authentication import (
    JWTAuthentication, 
    create_access_token, 
    create_refresh_token,
    decode_refresh_token
)

# Utilidades
import datetime
import random
import string

class RegisterAPIView(APIView):
    """End-point para registrar usuario."""
    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Las contraseñas no coinciden.')

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data)

class LoginAPIView(APIView):
    """End-point para el login de usuario."""
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Este correo electrónico no tiene cuenta.')
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Contraseña incorrecta.')
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        UserToken.objects.create(
            user_id = user.id,
            token = refresh_token,
            expired_at = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        )

        response = Response()

        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, samesite='None', secure=True)
        # response.headers = {
        #     'Set-Cookie': 'refresh_token={}; Path=/;HttpOnly;SameSite=None;Secure=true;'.format(refresh_token)
        # }
        response.data = {
            'token' : access_token,
            'refresh_token' : refresh_token
        }
        return response

class UserAPIView(APIView):
    """End-Point para enviar la información de usuairo solo si se envía un access token válido."""
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

class RefreshAPIView(APIView):
    """Vista para retornar un access_token por medio del refresh_token"""
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        if not UserToken.objects.filter(
            user_id=id, 
            token=refresh_token, 
            expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).exists():
            raise exceptions.AuthenticationFailed('No autenticado.')

        access_token = create_access_token(id)

        return Response({
            'token': access_token
        })

class LogoutAPIView(APIView):
    """Vista para eliminar de las cookies y de la base de datos los token de un usuario."""
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        UserToken.objects.filter(token=refresh_token).delete()
        response = Response()
        response.delete_cookie(key='refresh_token')

        response.data = {
            'message' : 'success'
        }

        return response

class ForgotAPIView(APIView):
    """Vista para enviar un mail con una url por la cual se puede cambiar la contraseña"""
    def post(self, request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        Reset.objects.create(
            email = email,
            token = token
        )

        url = 'http://localhost:3000/reset/' + token
        
        send_mail(
            subject='Cambio de contraseña',
            message='Click <a href="%s">aquí</a> para cambiar tu contraseña' % url,
            from_email='agendamiento.shaio2@gmail.com',
            recipient_list=[email]
        )

        return Response({
            'message': 'success'
        })

class ResetAPIView(APIView):
    """Vista para cambiar la contraseña"""
    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Las contraseñas no coinciden.')

        reset_password = Reset.objects.filter(token=data['token']).first()
        
        if not reset_password:
             raise exceptions.APIException('Enlace no válido')
            
        user = User.objects.filter(email=reset_password.email).first()

        if not user:
            raise exceptions.APIException('Usuario no encontrado')

        user.set_password(data['password'])
        user.save()

        return Response({
            'message':'success'
        })