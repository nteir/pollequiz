from django.urls import path
from pollequiz.api import views


app_name = 'api'
urlpatterns = [
    path('', views.api_home, name='api_home')
]
