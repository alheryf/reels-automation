import os
import google.generativeai as genai

# قراءة مفتاح الذكاء الاصطناعي من الإعدادات الآمنة
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def analyze_video_with_ai(video_title):
    print(f"جارٍ تحليل الفيديو ذكياً: {video_title}")
    # استخدام النموذج المحدث
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"اقترح أفضل 3 أجزاء مثيرة في فيديو يوتيوب عنوانه: {video_title} لتحويلها إلى مقاطع Reels قصيرة."
    response = model.generate_content(prompt)
    print("نتيجة تحليل الذكاء الاصطناعي:")
    print(response.text)

if __name__ == "__main__":
    print("بدء تشغيل نظام الأتمتة السحابي...")
    analyze_video_with_ai("فيديو تجريبي للاختبار المؤتمت")
