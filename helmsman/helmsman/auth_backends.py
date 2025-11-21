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
    Sets Django permissions based on PostgreSQL roles.
    """
    
    # Define which PostgreSQL roles map to Django permissions
    ADMIN_ROLES = ['postgres', 'admin', 'superuser', 'ribbon_admin', 'helmsman_admin']  # Modify these role names as needed
    STAFF_ROLES = ['staff', 'manager', 'faculty', 'ribbon_staff', 'helmsman_staff']      # Modify these role names as needed
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by attempting to connect to the SIS PostgreSQL database.
        If successful, create or update a Django user with permissions based on PG roles.
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
            
            # Get user's PostgreSQL roles
            roles = self.get_user_roles(connection, username)
            connection.close()
            
            # Determine Django permissions based on PG roles
            is_superuser = any(role in self.ADMIN_ROLES for role in roles)
            is_staff = is_superuser or any(role in self.STAFF_ROLES for role in roles)
            
            # Authentication successful - store credentials in session
            if request:
                request.session['sis_username'] = username
                request.session['sis_password'] = password
            
            # Get or create Django user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'is_staff': is_staff,
                    'is_superuser': is_superuser,
                }
            )
            
            # Update existing user permissions based on current roles
            if not created:
                if user.is_staff != is_staff or user.is_superuser != is_superuser:
                    user.is_staff = is_staff
                    user.is_superuser = is_superuser
                    user.save()
            
            return user
            
        except psycopg2.OperationalError as e:
            # Authentication failed - invalid credentials or connection error
            return None
        except Exception as e:
            # Other errors
            return None
    
    def get_user_roles(self, connection, username):
        """
        Query PostgreSQL to get all roles/groups the user belongs to.
        Returns a list of role names.
        """
        roles = []
        try:
            cursor = connection.cursor()
            
            # Query to get all roles the user is a member of
            query = """
                SELECT r.rolname
                FROM pg_roles r
                JOIN pg_auth_members m ON r.oid = m.roleid
                JOIN pg_roles u ON m.member = u.oid
                WHERE u.rolname = %s
                UNION
                SELECT rolname
                FROM pg_roles
                WHERE rolname = %s;
            """
            
            cursor.execute(query, (username, username))
            roles = [row[0] for row in cursor.fetchall()]
            cursor.close()
            
        except Exception as e:
            # If we can't query roles, return empty list (user gets no special permissions)
            pass
        
        return roles
    
    def get_user(self, user_id):
        """
        Get a user by ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
