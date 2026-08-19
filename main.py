import os
from google import genai

# جلب المفتاح الآمن
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    print("جاري الاتصال بالذكاء الاصطناعي...")
    # استخدام أحدث نموذج متوافق مع المكتبة الجديدة
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents="اقترح أفضل 3 أجزاء مثيرة في فيديو يوتيوب عن التكنولوجيا لتحويلها إلى مقاطع Reels قصيرة."
    )
    
    print("✨ نتيجة التحليل والرد:")
    print(response.text)
    
except Exception as e:
    print(f"حدث خطأ أثناء التشغيل: {e}")
