"""
URL configuration for helmsman project.
Place this file in /srv/ribbon2helmsman/helmsman/helmsman/urls.py
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CAS authentication URLs
    path('accounts/login/', 
         include('django_cas_ng.urls'), 
         name='cas_ng_login'),
    path('accounts/logout/', 
         include('django_cas_ng.urls'), 
         name='cas_ng_logout'),
    
    # Redirect root to a default view (customize as needed)
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
]
