import os
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY")
print(f"طول مفتاح الـ API الموجود: {len(API_KEY) if API_KEY else 'غير موجود'}")

try:
    genai.configure(api_key=API_KEY)
    print("محاولة الاتصال بالذكاء الاصطناعي...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("مرحباً، اختبار اتصال بسيط")
    print("✨ نجح الاتصال والرد بنجاح:")
    print(response.text)
except Exception as e:
    print(f"❌ حدث خطأ تفصيلي: {e}")
