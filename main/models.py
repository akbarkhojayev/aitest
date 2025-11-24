from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class Test(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tests')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    
    def __str__(self):
        return f"{self.test.title} - {self.question_text[:50]}"

class TestAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.test.title} - {self.score}/{self.total_questions}"

class Answer(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.attempt.student.username} - Q{self.question.id}"

class AIAnalysis(models.Model):
    attempt = models.OneToOneField(TestAttempt, on_delete=models.CASCADE, related_name='ai_analysis')
    analysis_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis for {self.attempt.student.username} - {self.attempt.test.title}"

class VideoLesson(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(help_text="YouTube video havolasi")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_video_id(self):
        """YouTube video ID ni olish"""
        if not self.video_url:
            return None
        
        try:
            if 'youtube.com/watch?v=' in self.video_url:
                return self.video_url.split('watch?v=')[1].split('&')[0]
            elif 'youtu.be/' in self.video_url:
                return self.video_url.split('youtu.be/')[1].split('?')[0]
            elif 'youtube.com/embed/' in self.video_url:
                return self.video_url.split('embed/')[1].split('?')[0]
            elif 'youtube.com/shorts/' in self.video_url:
                return self.video_url.split('shorts/')[1].split('?')[0]
        except Exception as e:
            print(f"Video ID olishda xato: {e}")
            return None
        
        return None
    
    def get_thumbnail_url(self):
        """YouTube video thumbnail rasmini olish"""
        video_id = self.get_video_id()
        if video_id:
            return f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
        return None
    
    def get_watch_url(self):
        """YouTube da ochish havolasi"""
        video_id = self.get_video_id()
        if video_id:
            return f'https://www.youtube.com/watch?v={video_id}'
        return self.video_url
