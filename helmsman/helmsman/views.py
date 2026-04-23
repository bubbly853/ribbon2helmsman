from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django import forms

class SISAuthForm(AuthenticationForm):
    def clean(self):
        try:
            return super().clean()
        except forms.ValidationError:
            error = getattr(self.request, '_auth_error', None)
            if error:
                raise forms.ValidationError(error)
            raise

class CustomLoginView(LoginView):
    form_class = SISAuthForm