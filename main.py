import os
import streamlit as st
from google import genai

st.set_page_config(page_title="YouTube Reels AI Factory", page_icon="🎬", layout="centered")

st.markdown("<h1 style='text-align: center;'>🎬 مصنع الريلز الذكي ليوتيوب</h1>", unsafe_allow_html=True)
st.write("---")
st.write("أدخل عنوان الفيديو أو فكرته، وسيقوم الذكاء الاصطناعي بتحليله وتصميم أفكار الـ Reels الاحترافية فوراً.")

# جلب المفتاح الآمن (يدعم إعدادات الويب وإعدادات السيرفر)
api_key = None
try:
    api_key = st.secrets.get("GEMINI_API_KEY")
except Exception:
    pass

if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY")

video_title = st.text_input("عنوان الفيديو أو الرابط:", placeholder="مثال: سر الاحتراف في المونتاج وكيف تطور قناتك...")

if st.button("🚀 ابدأ استخراج أفكار الريلز", type="primary"):
    if not api_key:
        st.error("الرجاء إضافة مفتاح Gemini API في إعدادات التطبيق.")
    elif not video_title:
        st.error("الرجاء كتابة عنوان الفيديو أولاً.")
    else:
        with st.spinner("جاري الاتصال بالسحابة وتحليل المحتوى بعين المخرج..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = (
                    f"أنت خبير محتوى ومونتاج سينمائي. بناءً على فيديو يوتيوب عنوانه: '{video_title}', "
                    "اقترح أفضل 3 أجزاء/لقطات مثيرة وجذابة يمكن تحويلها إلى مقاطع Reels قصيرة، "
                    "مع تحديد جملة الجذب (Hook)، وسبب الاختيار، وطريقة العرض."
                )
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                
                st.success("✨ تم إنشاء أفكار الريلز بنجاح!")
                st.markdown("### النتائج المقترحة:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")

st.write("---")
st.caption("تم تطوير هذا التطبيق خصيصاً لأتمتة صناعة المحتوى بسلاسة.")
