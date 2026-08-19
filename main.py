import os
import subprocess
import sys

print("جاري إعداد بيئة التشغيل...")
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], stdout=subprocess.DEVNULL)

deno_bin = os.path.expanduser("~/.deno/bin/deno")
if not os.path.exists(deno_bin):
    subprocess.run("curl -fsSL https://deno.land/install.sh | sh", shell=True, stdout=subprocess.DEVNULL)
os.environ["PATH"] += f":{os.path.expanduser('~/.deno/bin')}"

import yt_dlp

def process_real_reel(youtube_url, start_seconds=10, duration=30):
    print(f"🚀 بدء محاولة جلب الفيديو: {youtube_url}")
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'remote_components': ['ejs:github'],  # هذا هو السطر الحاسم لتفعيل حل الحماية عبر Deno
    }
    
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        print("🔑 تم استخدام ملف الكوكيز بنجاح.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_stream_url = info['url']
            video_title = info.get('title', 'فيديو يوتيوب')
            print(f"✨ تم جلب الفيديو بنجاح: {video_title}")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الاتصال بيوتيوب: {e}")
        return

    output_filename = "final_reel.mp4"
    
    # أمر مونتاج وقص الفيديو للأبعاد العمودية (9:16) عبر FFmpeg
    ffmpeg_cmd = [
        'ffmpeg',
        '-ss', str(start_seconds),
        '-i', video_stream_url,
        '-t', str(duration),
        '-vf', 'crop=ih*9/16:ih',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-y',
        output_filename
    ]
    
    print("🎬 جاري قص الفيديو ومونتاجه عمودياً عبر FFmpeg...")
    result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode == 0:
        print(f"✅ تم إنتاج الـ Reel بنجاح تام! الملف الناتج: {output_filename}")
    else:
        print(f"❌ حدث خطأ أثناء المونتاج بـ FFmpeg:")
        print(result.stderr)

if __name__ == "__main__":
    test_youtube_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    process_real_reel(test_youtube_url, start_seconds=5, duration=15)
