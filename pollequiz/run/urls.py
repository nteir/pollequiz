from django.urls import path
from pollequiz.run import views


app_name = 'run'
urlpatterns = [
    path('', views.QuizListView.as_view(), name='quiz_list'),
    path('<int:quiz_id>/', views.TakeFirstPage.as_view(), name='quiz_start'),
]
