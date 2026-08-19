import os
import sys
import json
import subprocess
import shutil

# 🛡️ [درع حماية 1] التحقق من أداة FFmpeg في النظام
def check_dependencies():
    if not shutil.which("ffmpeg"):
        print("❌ خطأ حرج: أداة ffmpeg غير مثبتة في النظام!")
        print("💡 يرجى التأكد من تشغيل خطوة تثبيت ffmpeg في ملف run.yml أولاً.")
        sys.exit(1)
    print("✅ أداة FFmpeg مثبتة وجاهزة للعمل.")

# 📄 [درع حماية 2] قراءة طلب المستخدم الديناميكي
def load_job_request():
    if os.path.exists("current_job.json"):
        try:
            with open("current_job.json", "r", encoding="utf-8") as f:
                job = json.load(f)
            print("📄 تم العثور على ملف الطلب current_job.json وقراءته بنجاح.")
            return job
        except Exception as e:
            print(f"⚠️ خطأ أثناء قراءة ملف current_job.json: {e}")
    
    # رابط فيسبوك افتراضي للاختبار فقط لو لم يتوفر ملف طلبات من الواجهة
    print("ℹ️ لم يتم العثور على current_job.json، سيتم استخدام رابط فيسبوك افتراضي للاختبار.")
    return {
        "url": "https://www.facebook.com/watch/?v=10153231379946729",
        "platform": "TikTok",
        "account": "default_account",
        "schedule": "Immediate"
    }

# 🌐 [درع حماية 3] سحب الفيديو من فيسبوك بكفاءة
def extract_facebook_stream(video_url):
    import yt_dlp

    print(f"\n📥 [1/3] جاري سحب رابط الفيديو من فيسبوك: {video_url}")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'noplaylist': True,
        'quiet': False,
        'no_warnings': True,
        'socket_timeout': 30,
        'retries': 5,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        print("🔑 تم تفعيل ملف cookies.txt لتجاوز القيود.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            stream_url = info.get('url')
            title = info.get('title', 'فيديو فيسبوك')
            print(f"✨ تم سحب الفيديو بنجاح! العنوان: {title}")
            return stream_url, title
    except Exception as e:
        print(f"❌ فشل سحب الفيديو من فيسبوك: {e}")
        return None, None

# 🧠 [درع حماية 4] تحليل Gemini مع خيار الآمان
def analyze_with_ai(title, api_key):
    if not api_key:
        print("⚠️ لم يتم العثور على GEMINI_API_KEY. سيتم تطبيق وقت قص افتراضي.")
        return [{"start": 5, "duration": 20, "hook": "مقطع مميز", "caption": "شاهد المقطع #reels"}]

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = (
            f"أنت خبير مونتاج. لدينا فيديو بعنوان '{title}'. "
            "اقترح وقتاً مناسباً لقص مقطع قصير مثير (Reel) مدته بين 15 و 30 ثانية. "
            "أرجِع النتيجة حصراً بصيغة JSON بدون أي نص إضافي للهيكل الآتي:\n"
            "[{\"start\": 5, \"duration\": 20, \"hook\": \"عنوان الخطاف\", \"caption\": \"وصف المقطع\"}]"
        )

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )

        clean_json = response.text.strip().replace("```json", "").replace("```", "")
        data = json.loads(clean_json)
        print("🧠 تم تحليل المقطع بواسطة Gemini 3.6 Flash بنجاح.")
        return data
    except Exception as e:
        print(f"⚠️ تعذر التحليل عبر الذكاء الاصطناعي ({e}). تم التبديل آلياً لوقت القص الآمن.")
        return [{"start": 5, "duration": 20, "hook": "مقطع آلي", "caption": "مقطع جديد #viral"}]

# 🎬 [درع حماية 5] القص والمونتاج العمودي بـ FFmpeg
def crop_and_cut(stream_url, clips):
    produced_files = []
    print("\n🎬 [2/3] بدء عملية القص والمونتاج العمودي (9:16)...")
    
    for index, clip in enumerate(clips):
        start = clip.get("start", 0)
        duration = clip.get("duration", 20)
        output_file = f"reel_{index + 1}.mp4"

        print(f"   -> قص المقطع {index + 1} (البداية: {start} ثانية، المدة: {duration} ثانية)...")

        ffmpeg_cmd = [
            'ffmpeg',
            '-ss', str(start),
            '-i', stream_url,
            '-t', str(duration),
            '-vf', 'crop=ih*9/16:ih',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-y',
            output_file
        ]

        res = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and os.path.exists(output_file):
            print(f"      ✅ تم إنتاج وحفظ: {output_file}")
            produced_files.append({"file": output_file, "info": clip})
        else:
            print(f"      ❌ فشل القص: {res.stderr}")

    return produced_files

# 🚀 التشغيل الأساسي
def main():
    print("🚀 [بدء الأتمتة] محرك التشغيل الشامل لروابط فيسبوك والمنصات...")
    check_dependencies()

    job = load_job_request()
    video_url = job.get("url")
    api_key = os.environ.get("GEMINI_API_KEY")

    stream_url, title = extract_facebook_stream(video_url)
    if not stream_url:
        print("❌ توقف التنفيذ بسبب تعذر استخراج رابط الفيديو.")
        sys.exit(1)

    clips = analyze_with_ai(title, api_key)
    results = crop_and_cut(stream_url, clips)

    if results:
        print(f"\n🎉 [3/3] اكتملت العملية بنجاح! تم إنتاج {len(results)} مقطع ريلز جاهز للنشر.")
    else:
        print("❌ لم يتم إنتاج أي مقاطع.")
        sys.exit(1)

if __name__ == "__main__":
    main()
