from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

User = get_user_model()


class HomeView(TemplateView):

    template_name = "index.html"
