from rest_framework import generics
from pollequiz.quiz.models import Quiz
from pollequiz.api.serializers import QuizSerializer, FullQuizSerializer


class QuizListAPIView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizAPIView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


# class FullQuizAPIView(generics.ListAPIView):
class FullQuizAPIView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = FullQuizSerializer
