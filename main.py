import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    print("جاري الاتصال بالذكاء الاصطناعي...")
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents="اقترح أفضل 3 أجزاء مثيرة في فيديو يوتيوب عن التكنولوجيا لتحويلها إلى مقاطع Reels قصيرة."
    )
    
    print("✨ نتيجة التحليل والرد:")
    print(response.text)
    
except Exception as e:
    print(f"حدث خطأ أثناء التشغيل: {e}")
