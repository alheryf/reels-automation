import os
import subprocess
import json

def main():
    print("🚀 بدء تشغيل السكربت بنجاح...")

    # قراءة الطلب من الواجهة أو الرابط الافتراضي
    if os.path.exists("current_job.json"):
        with open("current_job.json", "r", encoding="utf-8") as f:
            job = json.load(f)
        youtube_url = job.get("url")
    else:
        youtube_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

    print(f"📥 جاري سحب الفيديو: {youtube_url}")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
    }
    
    # استخدام ملف الكوكيز إن وجد لتجاوز حظر يوتيوب
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        print("🔑 تم استخدام ملف الكوكيز المرفق.")

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_stream_url = info['url']
            print(f"✨ تم سحب الرابط بنجاح: {info.get('title')}")
    except Exception as e:
        print(f"❌ فشل السحب بسبب قيود يوتيوب على السيرفر: {e}")
        return

    # قص الفيديو باستخدام FFmpeg المثبت نظامياً
    output_filename = "final_reel.mp4"
    print("🎬 جاري قص الفيديو عمودياً عبر FFmpeg...")
    
    ffmpeg_cmd = [
        'ffmpeg', '-ss', '10', '-i', video_stream_url, '-t', '20',
        '-vf', 'crop=ih*9/16:ih', '-c:v', 'libx264', '-c:a', 'aac', '-y', output_filename
    ]
    
    res = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"✅ تم إنتاج الـ Reel بنجاح تام: {output_filename}")
    else:
        print(f"❌ خطأ في المونتاج: {res.stderr}")

if __name__ == "__main__":
    main()
