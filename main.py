import os
import subprocess
import yt_dlp
from google import genai

# جلب مفتاح الذكاء الاصطناعي
api_key = os.environ.get("GEMINI_API_KEY")

def process_real_reel(youtube_url, start_seconds=10, duration=30):
    print(f"🚀 بدء الاتصال وتحميل بيانات الفيديو: {youtube_url}")
    
    # 1. استخدام yt-dlp لاستخراج رابط البث المباشر للفيديو دون تحميل الملف بالكامل ببطء
    ydl_opts = {'format': 'best[ext=mp4]/best'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_stream_url = info['url']
            video_title = info.get('title', 'فيديو يوتيوب')
            print(f"✨ تم العثور على الفيديو بنجاح: {video_title}")
    except Exception as e:
        print(f"❌ فشل في جلب الفيديو: {e}")
        return

    # 2. استخدام FFmpeg (المثبت مسبقاً على السيرفر) لقص الفيديو وتحويله لمقاس Reels (9:16) عمودي
    output_filename = "final_reel.mp4"
    
    # أمر المونتاج والقص:
    # -ss: وقت البداية بالثواني
    # -t: المدة المطلوبة للمقاطع (مثلاً 30 ثانية)
    # -vf "crop=ih*9/16:ih": قص العرض تلقائياً ليصبح عمودياً 9:16 بغض النظر عن أبعاد الفيديو الأصلي
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
        # هنا سيتم لاحقاً حفظه أو رفعه، الملف جاهز الآن كملف فيديو حقيقي `.mp4`
    else:
        print(f"❌ حدث خطأ أثناء المونتاج والقص:")
        print(result.stderr)

if __name__ == "__main__":
    # رابط فيديو تجريبي من يوتيوب لتجربة القص الفعلي
    test_youtube_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    
    # قص مقطع يبدأ من الثانية 5 ولمدة 15 ثانية وتحويله لـ Reel
    process_real_reel(test_youtube_url, start_seconds=5, duration=15)
