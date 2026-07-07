import os
import requests
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image

# 🔴 ضع بيانات تليجرام الخاصة بك هنا
TELEGRAM_TOKEN = "8648149189:AAH393Y1q2O8JXHGm4gP0cyE-tCgO2PCA78"
TELEGRAM_CHAT_ID = "715745079"

# رابط رادار الأمطار التابع للأرصاد الجوية العمانية (كمثال للمجمع البري)
BASE_URL = "https://www.caa.gov.om/weather/radar/composite" 

# 🔍 أبعاد الزوم والقص بالبكسل الخاصة بخريطة عمان (اليسار، الأعلى، اليمين، الأسفل)
# قم بتعديل هذه الأرقام لاحقاً لتحديد محافظتك بدقة (مثلاً للتركيز على شمال الباطنة ومسقط)
CROP_BOX = (300, 200, 700, 600) 

def download_radar_images():
    images = []
    now = datetime.utcnow()
    
    # رادار عمان يتحدث غالباً كل 6 إلى 10 دقائق
    for i in range(0, 60, 10): 
        time_slot = now - timedelta(minutes=i)
        minutes = (time_slot.minute // 10) * 10
        # تنسيق الوقت المعتمد في تسمية ملفات رادار عمان
        time_str = time_slot.strftime(f"%Y%m%d%H{minutes:02d}") 
        img_url = f"{BASE_URL}/oman_radar_{time_str}.png"
        
        try:
            response = requests.get(img_url, timeout=10)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                
                # ✂️ قص الصورة لعمل الزوم على المنطقة العمانية المحددة
                cropped_img = img.crop(CROP_BOX)
                images.append(cropped_img)
        except:
            continue
            
    return images[::-1]

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAnimation"
    caption_text = f"🔍 رادار الأمطار المحدث (زوم) - سلطنة عمان 🇴🇲\n⏰ التوقيت: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}"
    
    with open(file_path, 'rb') as file:
        payload = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption_text}
        files = {'animation': file}
        requests.post(url, data=payload, files=files)

def create_gif():
    imgs = download_radar_images()
    if imgs:
        output_filename = "oman_radar_zoom.gif"
        imgs[0].save(
            output_filename,
            save_all=True,
            append_images=imgs[1:],
            duration=400,
            loop=0        
        )
        send_to_telegram(output_filename)
        print("تم إرسال رادار عمان بنجاح!")
    else:
        print("لم يتم العثور على صور حديثة لرادار عمان، تأكد من روابط المصدر.")

if __name__ == "__main__":
    create_gif()
