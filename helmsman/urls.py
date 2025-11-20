from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
import django_cas_ng.views as cas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', cas_views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout/', cas_views.LogoutView.as_view(), name='cas_ng_logout'),
    path('accounts/callback/', cas_views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
    path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
]
