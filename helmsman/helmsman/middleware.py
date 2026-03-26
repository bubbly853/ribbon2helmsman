"""
Custom middleware for dynamic SIS database connection based on logged-in user
Place this file in /srv/ribbon2helmsman/helmsman/helmsman/middleware.py
"""

from django.conf import settings
from django.db import connections
from django.db import OperationalError
from django.http import HttpResponse
from django.template.loader import render_to_string
import re

class SISConnectionMiddleware:
    """
    Middleware to dynamically set SIS database credentials based on the logged-in user.
    This allows each user to connect to the SIS database with their own credentials.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Set SIS database credentials if user is authenticated
        if request.user.is_authenticated:
            # Get credentials from session (stored during login)
            username = request.session.get('sis_username')
            password = request.session.get('sis_password')
            
            if username and password:
                # Update the SIS database connection settings
                sis_db = connections.databases['sis']
                sis_db['USER'] = username
                sis_db['PASSWORD'] = password
                
                # Close existing connection to force reconnection with new credentials
                if 'sis' in connections:
                    connections['sis'].close()
        
        response = self.get_response(request)
        return response

class DatabaseAvailabilityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except OperationalError as e:
            context = {
                "service": self._parse_service(e),
                "detail": str(e).strip(),
            }
            html = render_to_string("503.html", context)
            return HttpResponse(html, status=503)

    def _parse_service(self, exc):
        msg = str(exc)
        if "5432" in msg or "postgresql" in msg.lower():
            return "PostgreSQL database"
        if "6379" in msg or "redis" in msg.lower():
            return "Redis"
        return "backend service"