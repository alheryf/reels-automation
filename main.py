import os
import time
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_with_retry():
    # قائمة النماذج للاستبدال الفوري في حال الضغط
    models_to_try = ['gemini-3.6-flash', 'gemini-1.5-flash']
    
    for model_name in models_to_try:
        for attempt in range(3):
            try:
                print(f"جاري الاتصال بالنموذج {model_name} (محاولة {attempt+1})...")
                response = client.models.generate_content(
                    model=model_name,
                    contents="اقترح أفضل 3 أجزاء مثيرة في فيديو يوتيوب عن التكنولوجيا لتحويلها إلى مقاطع Reels قصيرة."
                )
                return response.text
            except Exception as e:
                print(f"تنبيه (محاولة فاشلة): {e}")
                time.sleep(3) # انتظار 3 ثواني قبل إعادة المحاولة
                
    raise Exception("فشلت جميع المحاولات المؤقتة بسبب ضغط السيرفرات.")

if __name__ == "__main__":
    try:
        print("بدء تشغيل النظام السحابي...")
        result = generate_with_retry()
        print("✨ نتيجة التحليل والرد بنجاح:")
        print(result)
    except Exception as e:
        print(f"خطأ نهائي: {e}")
