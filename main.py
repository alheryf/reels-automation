import os
import subprocess
import sys
import json

# دالة لتثبيت الأدوات الأساسية التي يتطلبها يوتيوب لتجاوز الحماية
def setup_environment():
    print("🛠️ جاري تجهيز بيئة تجاوز الحماية...")
    # تحديث المكتبات
    subprocess.run([sys.executable, "-m", "pip", "install", "-U", "yt-dlp", "google-genai"], check=True)
    # تثبيت Deno لتجاوز الـ n-challenge
    if not os.path.exists("deno"):
        subprocess.run("curl -fsSL https://deno.land/install.sh | sh", shell=True, stdout=subprocess.DEVNULL)
        # إضافة المسار
        os.environ["PATH"] += f":{os.path.expanduser('~/.deno/bin')}"

def main():
    setup_environment()
    
    # قراءة الطلب (أو وضع رابط تجريبي)
    if os.path.exists("current_job.json"):
        with open("current_job.json", "r", encoding="utf-8") as f:
            job = json.load(f)
        youtube_url = job.get("url")
    else:
        youtube_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

    print(f"📥 جاري محاولة سحب الفيديو (بوضع المتصفح الخفي): {youtube_url}")

    # إعدادات السحب الذكية لتجاوز الـ Bot Detection
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        # هذه الإضافات هي "المفتاح" لتجاوز خطأ n challenge
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['dash', 'hls']
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_stream_url = info['url']
            print(f"✨ تم سحب الرابط بنجاح: {info.get('title')}")
            
            # (هنا تكمل كود القص والنشر الخاص بك...)
            print("🚀 تم تجاوز الحماية بنجاح، يمكنك الآن متابعة عمليات المونتاج.")
            
    except Exception as e:
        print(f"❌ فشل السحب حتى مع التحديثات: {e}")
        # إذا فشل السحب، فهذا يعني أن IP السيرفر محظور من يوتيوب حالياً
        print("💡 نصيحة: إذا استمرت المشكلة، يرجى إضافة ملف cookies.txt في المجلد.")

if __name__ == "__main__":
    main()
