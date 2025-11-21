"""
Custom authentication backend for PostgreSQL SIS database authentication
Place this file in /srv/ribbon2helmsman/helmsman/helmsman/auth_backends.py
"""

import psycopg2
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.conf import settings


class PostgreSQLAuthBackend(BaseBackend):
    """
    Authenticate against the PostgreSQL SIS database.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by attempting to connect to the SIS PostgreSQL database.
        If successful, create or update a Django user.
        """
        if username is None or password is None:
            return None
        
        # Try to connect to the SIS database with provided credentials
        try:
            connection = psycopg2.connect(
                host=settings.DATABASES['sis']['HOST'],
                port=settings.DATABASES['sis']['PORT'],
                database=settings.DATABASES['sis']['NAME'],
                user=username,
                password=password,
                connect_timeout=5
            )
            connection.close()
            
            # Authentication successful - store credentials in session
            if request:
                request.session['sis_username'] = username
                request.session['sis_password'] = password
            
            # Get or create Django user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'is_staff': False,
                    'is_superuser': False,
                }
            )
            
            # Update last login
            if not created:
                user.save()
            
            return user
            
        except psycopg2.OperationalError as e:
            # Authentication failed - invalid credentials or connection error
            return None
        except Exception as e:
            # Other errors
            return None
    
    def get_user(self, user_id):
        """
        Get a user by ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
