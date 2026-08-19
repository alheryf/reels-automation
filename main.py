import os
import subprocess
import sys
import json

def main():
    print("🚀 بدء التشغيل مع نظام تجاوز الحظر وتفعيل الـ Proxy...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-U", "yt-dlp", "google-genai"], stdout=subprocess.DEVNULL)

    # قراءة الطلب من الواجهة أو استخدام الرابط الافتراضي
    if os.path.exists("current_job.json"):
        with open("current_job.json", "r", encoding="utf-8") as f:
            job = json.load(f)
        youtube_url = job.get("url")
    else:
        youtube_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

    # جلب البروكسي من الـ Secrets إن وجد
    proxy_url = os.environ.get("PROXY_URL", "")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'web'],  # عميل iOS يتجاوز الحظر بكفاءة عالية
            }
        }
    }

    if proxy_url:
        ydl_opts['proxy'] = proxy_url
        print("🌐 تم تفعيل الـ Proxy المخصص بنجاح.")

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_stream_url = info['url']
            print(f"✨ تم سحب الفيديو بنجاح تام! العنوان: {info.get('title')}")

            # مرحلة القص الآلي الفوري عبر FFmpeg
            output_filename = "final_reel.mp4"
            print("🎬 جاري قص الفيديو عمودياً (9:16) عبر FFmpeg...")
            
            ffmpeg_cmd = [
                'ffmpeg', '-ss', '10', '-i', video_stream_url, '-t', '20',
                '-vf', 'crop=ih*9/16:ih', '-c:v', 'libx264', '-c:a', 'aac', '-y', output_filename
            ]
            
            res = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                print(f"✅ تم إنتاج الـ Reel بنجاح وأصبح جاهزاً للنشر: {output_filename}")
            else:
                print(f"❌ خطأ في المونتاج: {res.stderr}")

    except Exception as e:
        print(f"❌ حدث خطأ أثناء السحب: {e}")

if __name__ == "__main__":
    main()
