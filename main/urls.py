from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-test/', views.create_test, name='create_test'),
    path('edit-test/<int:test_id>/', views.edit_test, name='edit_test'),
    path('delete-test/<int:test_id>/', views.delete_test, name='delete_test'),
    path('add-questions/<int:test_id>/', views.add_questions, name='add_questions'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('take-test/<int:test_id>/', views.take_test, name='take_test'),
    path('test-result/<int:attempt_id>/', views.test_result, name='test_result'),
    path('view-results/<int:test_id>/', views.view_test_results, name='view_test_results'),
]
