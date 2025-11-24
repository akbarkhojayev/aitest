# 🎓 Django Test Tizimi - AI Tahlil va Video Darslar

Professional test tizimi Django fullstack loyihasi. Teacher va Student uchun alohida interfeys, AI tahlil, video darslar va zamonaviy dizayn.

## Xususiyatlar

✅ **Foydalanuvchi tizimi:**
- Teacher va Student ro'yxatdan o'tish
- Xavfsiz kirish tizimi
- Profil boshqaruvi

✅ **Teacher funksiyalari:**
- Test yaratish, tahrirlash, o'chirish
- Savollar qo'shish va boshqarish
- O'quvchilar natijalarini ko'rish
- Statistika va hisobotlar

✅ **Student funksiyalari:**
- Mavjud testlarni ko'rish
- Test topshirish
- Natijalarni ko'rish
- AI tahlil va tavsiyalar olish

✅ **AI Tahlil:**
- Haqiqiy AI (Groq/ChatGPT) orqali tahlil
- Har bir xato uchun batafsil tushuntirish
- Qaysi mavzuni o'rganish kerakligi
- Aniq tavsiyalar va yo'l-yo'riq

## O'rnatish

1. Virtual muhit yaratish:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

2. Kerakli paketlarni o'rnatish:
```bash
pip install -r requirements.txt
```

3. AI API kalitini olish (MUHIM!):

**Groq API (TAVSIYA ETILADI - bepul va juda tez):**
```
1. https://console.groq.com/ ga kiring
2. Sign up qiling (GitHub yoki Google orqali)
3. API Keys bo'limiga o'ting
4. "Create API Key" tugmasini bosing
5. Kalitni nusxalang (gsk_ bilan boshlanadi)
6. core/settings.py faylida GROQ_API_KEY ga kiriting
```

**Yoki OpenAI API (ChatGPT - pullik):**
```
1. https://platform.openai.com/ ga kiring
2. API Keys bo'limidan kalit yarating
3. core/settings.py da OPENAI_API_KEY ga kiriting
```

**Yoki DeepSeek API (arzon):**
```
1. https://platform.deepseek.com/ ga kiring
2. API key yarating
3. core/settings.py da DEEPSEEK_API_KEY ga kiriting
```

**ESLATMA:** Kamida bitta API kalitni to'g'ri kiritmasangiz, AI tahlil ishlamaydi!

4. Ma'lumotlar bazasini yaratish:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Admin foydalanuvchi yaratish:
```bash
python manage.py createsuperuser
```

6. Serverni ishga tushirish:
```bash
python manage.py runserver
```

7. Brauzerda ochish:
```
http://127.0.0.1:8000/
```

## Foydalanish

### Teacher uchun:
1. Ro'yxatdan o'ting (user_type: teacher)
2. Dashboard dan "Yangi Test Yaratish" tugmasini bosing
3. Test ma'lumotlarini kiriting
4. Savollar qo'shing (A, B, C, D variantlar bilan)
5. O'quvchilar natijalarini kuzating

### Student uchun:
1. Ro'yxatdan o'ting (user_type: student)
2. Mavjud testlardan birini tanlang
3. Testni bajaring
4. Natijalar va AI tahlilni ko'ring
5. Tavsiyalarga amal qiling

## Texnologiyalar

- **Backend:** Django 5.2.8
- **Frontend:** HTML, CSS (Hemis dizayni)
- **Database:** SQLite (development)
- **AI:** Groq API / OpenAI API
- **Authentication:** Django Auth

## 🤖 AI Tahlil Xususiyatlari

AI har bir savolni chuqur tahlil qilib quyidagilarni beradi:

### Har bir xato uchun:

1. **Savolni tahlil qilish:**
   - Savol nimani so'rayapti?
   - Qaysi bilim tekshirilmoqda?
   - Qiyinlik darajasi

2. **Barcha variantlarni tahlil qilish:**
   - ✅ To'g'ri javob: Nima uchun to'g'ri? (batafsil)
   - ❌ Noto'g'ri variantlar: Har biri nima uchun noto'g'ri?
   - Ko'p o'quvchilar nima uchun xato qilishi mumkin?

3. **O'quvchining xatosini tahlil qilish:**
   - Nima uchun aynan shu variantni tanlagan?
   - Qaysi bilim yetishmayapti?
   - Qanday mantiqiy xato qilgan?
   - Ehtiyotsizlikmi yoki bilim kamchiligi?

4. **To'g'ri javobni tushuntirish:**
   - Nima uchun to'g'ri?
   - Qanday mantiq asosida?
   - Misol va analogiyalar

5. **Aniq o'rganish tavsiyalari:**
   - Qaysi mavzuni o'rganish kerak?
   - Qaysi manbalardan foydalanish?
   - Qanday mashqlar bajarish?
   - Nimaga e'tibor berish?

6. **Umumiy baho va motivatsiya:**
   - Natijaga baho
   - Kuchli tomonlar
   - Zaif tomonlar
   - Keyingi qadamlar
   - Motivatsion xabar

## Loyiha Strukturasi

```
test/
├── core/                 # Asosiy sozlamalar
│   ├── settings.py      # Django sozlamalari
│   └── urls.py          # Asosiy URL marshrutlar
├── main/                # Asosiy ilova
│   ├── models.py        # Ma'lumotlar modellari
│   ├── views.py         # View funksiyalar
│   ├── urls.py          # URL marshrutlar
│   ├── admin.py         # Admin panel
│   └── templatetags/    # Custom template tags
├── templates/           # HTML shablonlar
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── teacher_dashboard.html
│   ├── student_dashboard.html
│   ├── create_test.html
│   ├── add_questions.html
│   ├── take_test.html
│   ├── test_result.html
│   └── ...
├── requirements.txt     # Python paketlar
└── README.md           # Bu fayl
```

## Muammolarni hal qilish

**AI tahlil ishlamayapti:**
- API kalitni tekshiring (`core/settings.py`)
- Internet aloqasini tekshiring
- API limitni tekshiring:
  - Groq: 30 req/min (bepul)
  - OpenAI: limitga qarab (pullik)
  - DeepSeek: 60 req/min
- Console da xatolarni ko'ring (`python manage.py runserver`)
- Agar API ishlamasa, oddiy tahlil ko'rsatiladi

**Ma'lumotlar bazasi xatosi:**
- `python manage.py makemigrations` bajaring
- `python manage.py migrate` bajaring

**Static fayllar yuklanmayapti:**
- `python manage.py collectstatic` bajaring

## Litsenziya

MIT License

## Muallif

Test Tizimi - Django Fullstack Loyihasi
