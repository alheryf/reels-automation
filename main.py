import os
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def run_ai():
    print("جاري الاتصال بالذكاء الاصطناعي...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "اقترح أفضل 3 أجزاء مثيرة في فيديو يوتيوب عن التكنولوجيا لتحويلها إلى مقاطع Reels قصيرة."
    response = model.generate_content(prompt)
    
    print("نتيجة التحليل:")
    print(response.text)

if __name__ == "__main__":
    print("بدء التشغيل بنجاح")
    run_ai()
