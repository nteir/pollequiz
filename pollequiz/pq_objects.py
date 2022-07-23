from django.contrib.auth.mixins import AccessMixin
from django.views.generic.base import ContextMixin
from django.shortcuts import redirect


class FailedAccessMixin(AccessMixin):
    """
    Overrides handle_no_permission to redirect
    instead of sending err code response.
    """
    redirect_url = ''

    def handle_no_permission(self):
        return redirect(self.redirect_url)


class PQFormContextMixin(ContextMixin):
    """
    Adds title and button text to forms.
    """
    title_text = ''
    btn_text = ''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_text
        context['button_text'] = self.btn_text
        return context
