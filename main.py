import os
import google.generativeai as genai

# قراءة مفتاح الذكاء الاصطناعي من الإعدادات الآمنة
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def analyze_video_with_ai(video_title):
    print(f"🎬 جارٍ تحليل الفيديو ذكياً: {video_title}")
    
    # استخدام نموذج فلاش الأحدث والأسرع
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = (
        f"أنت خبير محتوى ومونتاج. بناءً على عنوان فيديو اليوتيوب التالي: '{video_title}', "
        "اقترح أفضل 3 أجزاء/لقطات مثيرة وجذابة يمكن تحويلها إلى مقاطع Reels قصيرة تناسب منصات التواصل، "
        "مع توضيح سبب اختيار كل جزء."
    )
    
    response = model.generate_content(prompt)
    print("\n✨ نتيجة تحليل الذكاء الاصطناعي واقتراحات الريلز:")
    print("-" * 50)
    print(response.text)
    print("-" * 50)

if __name__ == "__main__":
    print("🚀 بدء تشغيل نظام أتمتة يوتيوب وسحابياً بنجاح...")
    # يمكنك تغيير العنوان لاحقاً بالفيديو الذي تريده
    analyze_video_with_ai("سر النجاح في صناعة المحتوى وكيف تطور قناتك بسرعة")
