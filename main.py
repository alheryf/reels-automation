import os
import subprocess
import sys
import json

def process_custom_request(youtube_url, target_platform, account_name, publish_time):
    print(f"🚀 بدء معالجة الرابط المطلوب: {youtube_url}")
    print(f"🎯 المنصة المستهدفة: {target_platform} | الحساب: {account_name} | وقت النشر: {publish_time}")

    # 1. إعداد البيئة صامتاً وسريعاً
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp", "google-genai"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    import yt_dlp
    from google import genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ خطأ: مفتاح الـ API غير موجود.")
        return

    client = genai.Client(api_key=api_key)

    # 2. سحب الفيديو المرسل
    print("📥 جاري سحب بيانات الفيديو من الرابط المحدد...")
    ydl_opts = {'format': 'best[ext=mp4]/best', 'noplaylist': True}
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_stream_url = info['url']
            video_title = info.get('title', 'فيديو')
            print(f"✨ تم جلب الفيديو بنجاح: {video_title}")
    except Exception as e:
        print(f"❌ فشل سحب الفيديو: {e}")
        return

    # 3. قص الفيديو عمودياً (أو الاعتماد على الذكاء الاصطناعي لاختيار الأوقات)
    output_filename = "final_reel.mp4"
    print("🎬 جاري قص المقطع عمودياً عبر FFmpeg...")
    
    # هنا يمكنك جعل أوقات البداية والنهاية متغيرة حسب رغبتك أو استخراجها بالذكاء الاصطناعي
    ffmpeg_cmd = [
        'ffmpeg', '-ss', '15', '-i', video_stream_url, '-t', '30',
        '-vf', 'crop=ih*9/16:ih', '-c:v', 'libx264', '-c:a', 'aac', '-y', output_filename
    ]
    
    res = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"✅ تم إنتاج الـ Reel بنجاح: {output_filename}")
        print(f"🚀 [محاكاة النشر] سيتم نشر هذا الفيديو على حساب ({account_name}) في منصة ({target_platform}) حسب جدول وقت النشر: {publish_time}")
    else:
        print(f"❌ خطأ في المونتاج: {res.stderr}")

if __name__ == "__main__":
    # إذا تم تمرير الرابط من خلال سطر الأوامر أو الواجهة، يتم استخدامه
    # وإلا يمكننا قراءته من ملف إعدادات الطلبات (Queue)
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        platform = sys.argv[2] if len(sys.argv) > 2 else "tiktok"
        account = sys.argv[3] if len(sys.argv) > 3 else "default_account"
        sched_time = sys.argv[4] if len(sys.argv) > 4 else "Immediate"
    else:
        # افتراضي للتجربة لو لم يُمرر شيء
        target_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        platform = "tiktok"
        account = "account_one"
        sched_time = "2026-08-19 18:00"

    process_custom_request(target_url, platform, account, sched_time)
