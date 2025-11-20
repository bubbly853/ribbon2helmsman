from django_cas_ng.backends import CASBackend
from django.contrib.auth.models import Group
import logging

logger = logging.getLogger(__name__)

class CASRoleBackend(CASBackend):
    def configure_user(self, user, attributes=None):
        """
        Map CAS attributes to Django groups/permissions
        Called when a user logs in via CAS for the first time or updates
        """
        user = super().configure_user(user, attributes)
        
        if attributes:
            logger.info(f"CAS attributes for {user.username}: {attributes}")
            
            # Extract attributes from CAS response
            # Adjust these based on your CAS server's attribute release
            cas_groups = attributes.get('groups', [])
            email = attributes.get('email', '')
            first_name = attributes.get('givenName', '')
            last_name = attributes.get('sn', '') or attributes.get('surname', '')
            
            # Update user info
            if email:
                user.email = email
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            
            # Clear existing groups
            user.groups.clear()
            
            # Map CAS groups to Django groups and permissions
            if 'admin' in cas_groups or 'helsman_admin' in cas_groups:
                admin_group, _ = Group.objects.get_or_create(name='Database Admin')
                user.groups.add(admin_group)
                user.is_staff = True
                user.is_superuser = True
                
            elif 'editor' in cas_groups or 'helsman_editor' in cas_groups:
                editor_group, _ = Group.objects.get_or_create(name='Database Editor')
                user.groups.add(editor_group)
                user.is_staff = True
                
            elif 'viewer' in cas_groups or 'helsman_viewer' in cas_groups:
                viewer_group, _ = Group.objects.get_or_create(name='Database Viewer')
                user.groups.add(viewer_group)
            
            else:
                # Default group for authenticated users
                default_group, _ = Group.objects.get_or_create(name='Authenticated Users')
                user.groups.add(default_group)
            
            user.save()
            logger.info(f"User {user.username} configured with groups: {[g.name for g in user.groups.all()]}")
        
        return user
