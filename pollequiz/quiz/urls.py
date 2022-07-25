from django.urls import path
from pollequiz.quiz import views

app_name = 'quiz'
urlpatterns = [
    path('', views.QuizListView.as_view(), name='list_all'),
    path('my/', views.QuizListView.as_view(), name='list_my'),
    path('new/', views.QuizCreateView.as_view(), name='new'),
    path('<int:pk>/', views.QuizDetailView.as_view(), name='quiz_card'),
    path('<int:pk>/update/', views.QuizUpdateView.as_view(), name='quiz_update'),
    path('<int:pk>/delete/', views.QuizDeleteView.as_view(), name='quiz_delete'),
]
