from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, Test, Question, TestAttempt, Answer, AIAnalysis
import json
import requests
from django.conf import settings

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu foydalanuvchi nomi band!')
            return redirect('register')
        
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, user_type=user_type)
        messages.success(request, 'Ro\'yxatdan o\'tdingiz!')
        return redirect('login')
    
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Login yoki parol xato!')
    
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    
    if profile.user_type == 'teacher':
        tests = Test.objects.filter(teacher=request.user)
        return render(request, 'teacher_dashboard.html', {'tests': tests})
    else:
        tests = Test.objects.all()
        attempts = TestAttempt.objects.filter(student=request.user).order_by('-completed_at')
        return render(request, 'student_dashboard.html', {'tests': tests, 'attempts': attempts})

@login_required
def create_test(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.user_type != 'teacher':
        messages.error(request, 'Faqat o\'qituvchilar test yarata oladi!')
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        test = Test.objects.create(teacher=request.user, title=title, description=description)
        messages.success(request, 'Test yaratildi! Endi savollar qo\'shing.')
        return redirect('add_questions', test_id=test.id)
    
    return render(request, 'create_test.html')

@login_required
def add_questions(request, test_id):
    test = get_object_or_404(Test, id=test_id, teacher=request.user)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        option_a = request.POST.get('option_a')
        option_b = request.POST.get('option_b')
        option_c = request.POST.get('option_c')
        option_d = request.POST.get('option_d')
        correct_answer = request.POST.get('correct_answer')
        
        Question.objects.create(
            test=test,
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer
        )
        messages.success(request, 'Savol qo\'shildi!')
        
        if 'add_more' in request.POST:
            return redirect('add_questions', test_id=test.id)
        else:
            return redirect('dashboard')
    
    questions = test.questions.all()
    return render(request, 'add_questions.html', {'test': test, 'questions': questions})

@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    profile = UserProfile.objects.get(user=request.user)
    
    if profile.user_type != 'student':
        messages.error(request, 'Faqat o\'quvchilar test topshira oladi!')
        return redirect('dashboard')
    
    questions = test.questions.all()
    
    if request.method == 'POST':
        attempt = TestAttempt.objects.create(
            student=request.user,
            test=test,
            total_questions=questions.count()
        )
        
        score = 0
        wrong_answers = []
        all_questions = []  # Barcha savollar AI tahlil uchun
        
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            if selected:
                is_correct = selected == question.correct_answer
                if is_correct:
                    score += 1
                
                # Har bir savolni AI tahlil uchun saqlash
                question_data = {
                    'question': question.question_text,
                    'correct': question.correct_answer,
                    'selected': selected,
                    'is_correct': is_correct,
                    'options': {
                        'A': question.option_a,
                        'B': question.option_b,
                        'C': question.option_c,
                        'D': question.option_d
                    }
                }
                all_questions.append(question_data)
                
                if not is_correct:
                    wrong_answers.append(question_data)
                
                Answer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_answer=selected,
                    is_correct=is_correct
                )
        
        attempt.score = score
        attempt.save()
        
        # AI tahlil yaratish (haqiqiy AI API bilan - barcha savollarni tahlil qilish)
        analysis = generate_ai_analysis_with_api(all_questions, wrong_answers, score, questions.count(), test.title)
        AIAnalysis.objects.create(attempt=attempt, analysis_text=analysis)
        
        messages.success(request, f'Test yakunlandi! Natija: {score}/{questions.count()}')
        return redirect('test_result', attempt_id=attempt.id)
    
    return render(request, 'take_test.html', {'test': test, 'questions': questions})

@login_required
def test_result(request, attempt_id):
    attempt = get_object_or_404(TestAttempt, id=attempt_id, student=request.user)
    answers = attempt.answers.all()
    ai_analysis = AIAnalysis.objects.filter(attempt=attempt).first()
    
    return render(request, 'test_result.html', {
        'attempt': attempt,
        'answers': answers,
        'ai_analysis': ai_analysis
    })

@login_required
def view_test_results(request, test_id):
    test = get_object_or_404(Test, id=test_id, teacher=request.user)
    attempts = TestAttempt.objects.filter(test=test).order_by('-completed_at')
    
    return render(request, 'view_test_results.html', {'test': test, 'attempts': attempts})

@login_required
def edit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, teacher=request.user)
    
    if request.method == 'POST':
        test.title = request.POST.get('title')
        test.description = request.POST.get('description')
        test.save()
        messages.success(request, 'Test muvaffaqiyatli yangilandi!')
        return redirect('dashboard')
    
    return render(request, 'edit_test.html', {'test': test})

@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, teacher=request.user)
    
    if request.method == 'POST':
        test_title = test.title
        test.delete()
        messages.success(request, f'"{test_title}" testi o\'chirildi!')
        return redirect('dashboard')
    
    return render(request, 'delete_test.html', {'test': test})

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    test = question.test
    
    if test.teacher != request.user:
        messages.error(request, 'Sizda bu savolni o\'chirish huquqi yo\'q!')
        return redirect('dashboard')
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Savol o\'chirildi!')
        return redirect('add_questions', test_id=test.id)
    
    return redirect('add_questions', test_id=test.id)

def generate_ai_analysis_with_api(all_questions, wrong_answers, score, total, test_title):
    """Haqiqiy AI API orqali tahlil yaratish - savollarni o'qib tahlil qilish"""
    
    # API kalitlarini settings.py dan olish
    groq_key = getattr(settings, 'GROQ_API_KEY', None)
    openai_key = getattr(settings, 'OPENAI_API_KEY', None)
    deepseek_key = getattr(settings, 'DEEPSEEK_API_KEY', None)
    
    percentage = (score / total) * 100
    
    # AI uchun batafsil prompt tayyorlash
    prompt = f"""Siz professional ta'lim mutaxassisi va test tahlilchisisiz. O'quvchi "{test_title}" testini topshirdi.

TEST NATIJALARI:
- Jami savollar: {total}
- To'g'ri javoblar: {score}
- Xato javoblar: {total - score}
- Foiz: {percentage:.1f}%

"""
    
    if wrong_answers:
        prompt += "XATO QILINGAN SAVOLLAR (BATAFSIL TAHLIL KERAK):\n\n"
        for idx, wrong in enumerate(wrong_answers, 1):
            prompt += f"═══════════════════════════════════════\n"
            prompt += f"XATO #{idx}\n"
            prompt += f"═══════════════════════════════════════\n\n"
            prompt += f"SAVOL: {wrong['question']}\n\n"
            prompt += f"VARIANTLAR:\n"
            for opt in ['A', 'B', 'C', 'D']:
                marker = "✅" if opt == wrong['correct'] else ("❌" if opt == wrong['selected'] else "  ")
                prompt += f"{marker} {opt}) {wrong['options'][opt]}\n"
            prompt += f"\nO'quvchi tanladi: {wrong['selected']} - {wrong['options'][wrong['selected']]}\n"
            prompt += f"To'g'ri javob: {wrong['correct']} - {wrong['options'][wrong['correct']]}\n\n"
    else:
        prompt += "🎉 O'quvchi barcha savollarga to'g'ri javob berdi!\n\n"
    
    prompt += """
VAZIFA: O'zbek tilida QISQA va ANIQ tahlil yozing.

HAR BIR XATO UCHUN:

1. SAVOL TAHLILI (1-2 jumla):
   - Savol nimani tekshirmoqda?

2. JAVOBLAR TAHLILI:
   - ✅ To'g'ri javob: Nima uchun to'g'ri? (1 jumla)
   - ❌ Sizning javobingiz: Nima uchun noto'g'ri? (1 jumla)

3. XATO SABABI (1 jumla):
   - Qaysi bilim yoki tushuncha yetishmayapti?

4. TAVSIYA (1-2 jumla):
   - Nimani o'rganish kerak?

UMUMIY BAHO:
- Natijaga qisqa baho (2-3 jumla)
- Asosiy tavsiya (1-2 jumla)

MUHIM:
- Har bir bo'lim QISQA bo'lsin (1-2 jumla)
- Aniq va tushunarli yozing
- Ortiqcha so'z ishlatmang
- Emoji ishlatishingiz mumkin

Javobni o'zbek tilida yozing!
"""
    
    # 1. Groq API (eng tez va bepul)
    if groq_key and groq_key != 'gsk_your_api_key_here':
        try:
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {groq_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'llama-3.3-70b-versatile',  # Yangilangan model
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'Siz professional ta\'lim mutaxassisi va test tahlilchisisiz. O\'zbek tilida aniq va foydali tahlillar berasiz.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': 0.7,
                    'max_tokens': 1500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"Groq API xatosi: {str(e)}")
    
    # 2. OpenAI API (ChatGPT)
    if openai_key and openai_key != 'sk-your_api_key_here':
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {openai_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'Siz professional ta\'lim mutaxassisi va test tahlilchisisiz. O\'zbek tilida aniq va foydali tahlillar berasiz.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': 0.7,
                    'max_tokens': 1500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"OpenAI API xatosi: {str(e)}")
    
    # 3. DeepSeek API
    if deepseek_key and deepseek_key != 'sk-your_api_key_here':
        try:
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {deepseek_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'deepseek-chat',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'Siz professional ta\'lim mutaxassisi va test tahlilchisisiz. O\'zbek tilida aniq va foydali tahlillar berasiz.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': 0.7,
                    'max_tokens': 1500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"DeepSeek API xatosi: {str(e)}")
    
    # Agar hech qaysi API ishlamasa, fallback
    return generate_ai_analysis_fallback(all_questions, wrong_answers, score, total)

def generate_ai_analysis_fallback(all_questions, wrong_answers, score, total):
    """API ishlamasa, oddiy tahlil (faqat xatolik holatida)"""
    percentage = (score / total) * 100
    
    analysis = "⚠️ AI TAHLIL XIZMATI VAQTINCHA ISHLAMAYAPTI\n\n"
    analysis += "═══════════════════════════════════════════════════\n"
    analysis += "           📊 ODDIY NATIJALAR\n"
    analysis += "═══════════════════════════════════════════════════\n\n"
    
    analysis += f"📈 UMUMIY NATIJA:\n"
    analysis += f"   • To'g'ri javoblar: {score}/{total}\n"
    analysis += f"   • Xato javoblar: {total - score}/{total}\n"
    analysis += f"   • Foiz: {percentage:.1f}%\n\n"
    
    if len(wrong_answers) > 0:
        analysis += "🔍 XATO QILINGAN SAVOLLAR:\n\n"
        for idx, wrong in enumerate(wrong_answers, 1):
            analysis += f"{idx}. SAVOL: {wrong['question']}\n"
            analysis += f"   ❌ Sizning javobingiz: {wrong['selected']} - {wrong['options'][wrong['selected']]}\n"
            analysis += f"   ✅ To'g'ri javob: {wrong['correct']} - {wrong['options'][wrong['correct']]}\n\n"
    
    analysis += "\n💡 ESLATMA:\n"
    analysis += "Batafsil AI tahlil olish uchun:\n"
    analysis += "1. Internet aloqangizni tekshiring\n"
    analysis += "2. Biroz kutib qayta urinib ko'ring\n"
    analysis += "3. Yoki admin bilan bog'laning\n\n"
    
    if percentage >= 80:
        analysis += "🎉 Yaxshi natija! Xato qilgan savollarni qayta ko'rib chiqing."
    elif percentage >= 60:
        analysis += "👍 O'rtacha natija. Ba'zi mavzularni takrorlang."
    else:
        analysis += "📚 Ko'proq mashq qilish va o'rganish kerak."
    
    return analysis

# Bu funksiya o'chirildi - faqat AI API ishlatiladi
