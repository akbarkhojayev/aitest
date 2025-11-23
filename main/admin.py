from django.contrib import admin
from .models import UserProfile, Test, Question, TestAttempt, Answer, AIAnalysis

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type']
    list_filter = ['user_type']

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'created_at']
    list_filter = ['created_at']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'question_text', 'correct_answer']
    list_filter = ['test']

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'test', 'score', 'total_questions', 'completed_at']
    list_filter = ['test', 'completed_at']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_answer', 'is_correct']
    list_filter = ['is_correct']

@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'created_at']
    list_filter = ['created_at']
