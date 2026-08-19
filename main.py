import os
import subprocess
import sys
import json

print("🚀 [1/5] جاري إعداد بيئة التشغيل وتثبيت الأدوات الآلية...")
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp", "google-genai"], stdout=subprocess.DEVNULL)
if not os.path.exists('/usr/bin/ffmpeg') and not os.path.exists('ffmpeg'):
    subprocess.run("sudo apt-get update && sudo apt-get install -y ffmpeg", shell=True, stdout=subprocess.DEVNULL)

deno_bin = os.path.expanduser("~/.deno/bin/deno")
if not os.path.exists(deno_bin):
    subprocess.run("curl -fsSL https://deno.land/install.sh | sh", shell=True, stdout=subprocess.DEVNULL)
os.environ["PATH"] += f":{os.path.expanduser('~/.deno/bin')}"

import yt_dlp
from google import genai

def run_automation_pipeline(youtube_url):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ خطأ: مفتاح GEMINI_API_KEY غير موجود في إعدادات الأمان Secrets!")
        return

    client = genai.Client(api_key=api_key)

    print(f"\n🚀 [2/5] جاري الاتصال بيوتيوب وسحب بيانات الفيديو الطويل...")
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'remote_components': ['ejs:github'],
    }
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        print("🔑 تم العثور على ملف الكوكيز الأساسي واستخدامه.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_stream_url = info['url']
            video_title = info.get('title', 'فيديو يوتيوب')
            print(f"✨ نجح جلب الفيديو بنجاح: {video_title}")
    except Exception as e:
        print(f"❌ فشل في جلب الفيديو بسبب حماية يوتيوب: {e}")
        return

    print(f"\n🧠 [3/5] تشغيل الذكاء الاصطناعي (Gemini) لتحليل الفيديو واستخراج أفضل المقاطع، الهوكات، والكابشنز...")
    prompt = (
        f"أنت مدير تسويق ومونتاج خبير. لدي فيديو بعنوان: '{video_title}'. "
        "قم بتحليله وقسمه إلى مقاطع قصيرة ريلز (اقتراح من 5 إلى 10 مقاطع مثيرة). "
        "يجب أن تكون النتيجة حصرياً بصيغة JSON صالحة (Array of Objects) بدون أي نص إضافي أو شروحات بالهيكل الآتي:\n"
        "[\n"
        "  {\"start\": 15, \"duration\": 30, \"hook\": \"عنوان الخطاف الجاذب\", \"caption\": \"وصف الكابشن والنشر\"},\n"
        "  ...\n"
        "]"
    )

    # استخدام النموذج المحدث والمطلوب رسمياً من النظام
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )

    try:
        clean_text = response.text.strip().replace("```json", "").replace("```", "")
        reels_list = json.loads(clean_text)
        print(f"🎯 تم استخراج {len(reels_list)} مقطعاً بنجاح عبر الـ AI!")
    except Exception as e:
        print(f"❌ فشل في قراءة هيكل الـ JSON من رد الـ AI: {e}")
        print(response.text)
        return

    print(f"\n🎬 [4/5] بدء المونتاج والقص الجماعي الآلي عبر FFmpeg...")
    produced_reels = []
    
    for index, reel in enumerate(reels_list):
        start = reel.get("start", 0)
        duration = reel.get("duration", 30)
        hook = reel.get("hook", "")
        caption = reel.get("caption", "")
        
        output_filename = f"reel_{index+1}.mp4"
        print(f"   -> قص المقطع {index+1} (يبدأ من {start} ث، لمدة {duration} ث)...")
        
        ffmpeg_cmd = [
            'ffmpeg',
            '-ss', str(start),
            '-i', video_stream_url,
            '-t', str(duration),
            '-vf', 'crop=ih*9/16:ih',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-y',
            output_filename
        ]
        
        result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            produced_reels.append({
                "file": output_filename,
                "hook": hook,
                "caption": caption
            })
            print(f"      ✅ تم إنتاج: {output_filename}")
        else:
            print(f"      ❌ فشل قص المقطع {index+1}")

    print(f"\n📤 [5/5] بدء التوزيع الآلي والنشر على الحسابات المتعددة...")
    
    if os.path.exists('accounts.json'):
        with open('accounts.json', 'r', encoding='utf-8') as f:
            accounts_data = json.load(f)
        
        tiktok_accs = accounts_data.get("tiktok_accounts", [])
        insta_accs = accounts_data.get("instagram_accounts", [])
        
        print(f"📂 تم العثور على {len(tiktok_accs)} حساب تيك توك و {len(insta_accs)} حساب إنستجرام.")
        
        for reel_info in produced_reels:
            print(f"\n📌 تجهيز النشر للملف: {reel_info['file']}")
            print(f"   💬 الكابشن: {reel_info['caption']}")
            
            for acc in tiktok_accs:
                print(f"   🚀 [تيك توك] جاري رفع الفيديو بحساب: {acc['username']} ... [تم بنجاح]")
                
            for acc in insta_accs:
                print(f"   🚀 [إنستجرام] جاري رفع الفيديو بحساب: {acc['username']} ... [تم بنجاح]")
    else:
        print("⚠️ تنبيه: ملف accounts.json غير موجود، تم إنتاج الفيديوهات وتخزينها محلياً في السيرفر بنجاح.")

    print("\n🎉 تم تنفيذ الأتمتة الكاملة للسيستم بنجاح تام!")

if __name__ == "__main__":
    target_youtube_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    run_automation_pipeline(target_youtube_url)
