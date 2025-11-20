"""
Custom middleware for dynamic SIS database connection based on logged-in user
Place this file in /srv/ribbon2helmsman/helmsman/helmsman/middleware.py
"""

from django.conf import settings
from django.db import connections

class DynamicSISConnectionMiddleware:
    """
    Middleware to dynamically set SIS database credentials based on the logged-in user.
    This allows each user to connect to the SIS database with their own credentials.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Set SIS database credentials if user is authenticated
        if request.user.is_authenticated:
            # Get the username from CAS
            username = request.user.username
            
            # You'll need to implement a method to retrieve the user's SIS password
            # This could be stored in a profile model, retrieved from CAS attributes,
            # or managed through another secure mechanism
            password = self.get_sis_password_for_user(username)
            
            if password:
                # Update the SIS database connection settings
                sis_db = connections.databases['sis']
                sis_db['USER'] = username
                sis_db['PASSWORD'] = password
                
                # Close existing connection to force reconnection with new credentials
                if 'sis' in connections:
                    connections['sis'].close()
        
        response = self.get_response(request)
        return response
    
    def get_sis_password_for_user(self, username):
        """
        Retrieve the SIS database password for the given user.
        
        IMPORTANT: Implement this method based on your security requirements.
        Options include:
        1. Store encrypted passwords in a UserProfile model
        2. Use CAS attributes if passwords are passed during authentication
        3. Use a separate credential management system
        4. Have users enter their SIS password on first login and store it securely
        
        For now, this returns None - you must implement this.
        """
        # TODO: Implement secure password retrieval
        # Example implementation using a UserProfile model:
        # try:
        #     from myapp.models import UserProfile
        #     profile = UserProfile.objects.get(user__username=username)
        #     return profile.decrypt_sis_password()
        # except UserProfile.DoesNotExist:
        #     return None
        
        return None
