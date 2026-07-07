import os
import requests
from datetime import datetime
from io import BytesIO
from PIL import Image

# 🔴 ضع بياناتك الصحيحة هنا
TELEGRAM_TOKEN = "8648149189:AAH393Y1q2O8JXHGm4gP0cyE-tCgO2PCA78"
TELEGRAM_CHAT_ID = "715745079"

# روابط لصور خرائط طقس حية ومستقرة جداً للتجربة والتأكد من عمل النظام
URLS = [
    "https://img.thewunderground.com/images/maps/current/mideast_radar.gif",
    "https://img.thewunderground.com/images/maps/current/mideast_satellite.gif"
]

def download_images():
    images = []
    # محاولة سحب صور حية للتأكد من الاتصال
    for url in URLS:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                # تحويل الصورة لصيغة RGB لضمان قبولها في القص والدمج
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # يمكنك تفعيل السطر أدناه إذا كنت تريد تجربة القص والزوم
                # img = img.crop((100, 100, 500, 500)) 
                
                images.append(img)
        except Exception as e:
            print(f"فشل تحميل الرابط بسبب: {e}")
            continue
    return images

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAnimation"
    caption_text = f"⚙️ اختبار نظام الرادار التلقائي المحدث\n⏰ التوقيت: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}"
    
    with open(file_path, 'rb') as file:
        payload = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption_text}
        files = {'animation': file}
        res = requests.post(url, data=payload, files=files)
        print("استجابة تليجرام:", res.text) # سيطبع لك بوضوح في الـ Actions إذا كان تليجرام يرفض الإرسال ولماذا

def create_gif():
    imgs = download_images()
    if len(imgs) >= 1:
        output_filename = "test_radar.gif"
        # دمج الصور
        imgs[0].save(
            output_filename,
            save_all=True,
            append_images=imgs[1:],
            duration=500,
            loop=0        
        )
        send_to_telegram(output_filename)
    else:
        print("خطأ: لم يتمكن الخادم من سحب أي صورة من الإنترنت.")

if __name__ == "__main__":
    create_gif()
