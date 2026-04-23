"""
URL configuration for helmsman project.
Place this file in /srv/ribbon2helmsman/helmsman/helmsman/urls.py
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from helmsman.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', 
         CustomLoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('accounts/logout/', 
         auth_views.LogoutView.as_view(),
         name='logout'),
    path('', include('sis.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
