"""
URL configuration for helmsman project.
Place this file in /srv/ribbon2helmsman/helmsman/helmsman/urls.py
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/login/', 
         auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('accounts/logout/', 
         auth_views.LogoutView.as_view(),
         name='logout'),
    
    # Redirect root to a default view (customize as needed)
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
]
