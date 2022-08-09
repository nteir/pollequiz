from rest_framework import serializers
from pollequiz.quiz.models import Quiz, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'a_number',
            'text',
            'correct',
        ]


class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'q_number',
            'q_type',
            'text',
            'points',
            'answer_set',
        ]


class QuizSerializer(serializers.ModelSerializer):
    url_detail = serializers.HyperlinkedIdentityField(view_name='api:quiz_detail', lookup_field='pk')
    url_full_quiz = serializers.HyperlinkedIdentityField(view_name='api:quiz_full', lookup_field='pk')
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'url_detail',
            'url_full_quiz',
            'pk',
            'name',
            'author',
            'author_username',
            'description',
            'created_at',
        ]


class FullQuizSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'name',
            'question_set',
        ]
        read_only_fields = [
            'name',
            'question_set',
        ]
