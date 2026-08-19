import os
import subprocess
import yt_dlp

def process_real_reel(youtube_url, start_seconds=10, duration=30):
    print(f"🚀 بدء الاتصال وتحميل بيانات الفيديو: {youtube_url}")
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
    }
    
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        print("🔑 تم العثور على ملف الكوكيز واستخدامه لتجاوز التحقق.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_stream_url = info['url']
            video_title = info.get('title', 'فيديو يوتيوب')
            print(f"✨ تم العثور على الفيديو بنجاح: {video_title}")
    except Exception as e:
        print(f"❌ فشل في جلب الفيديو بسبب الحظر: {e}")
        return

    output_filename = "final_reel.mp4"
    
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
    result = subprocess.run(ffmpeg_cmd, captureoutput=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ تم إنتاج الـ Reel بنجاح تام! الملف الناتج: {output_filename}")
    else:
        print(f"❌ حدث خطأ أثناء المونتاج والقص:")
        print(result.stderr)

if __name__ == "__main__":
    test_youtube_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    process_real_reel(test_youtube_url, start_seconds=5, duration=15)
