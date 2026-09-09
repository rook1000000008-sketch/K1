import json
import urllib.request
import os

FIREBASE_DB_URL = "https://kmart-cf668-default-rtdb.asia-southeast1.firebasedatabase.app/"

def push_all_to_firebase():
    departments = ["01sp", "02fn", "03en", "04ed", "05sw", "06ph"]
    all_materials = {}

    for dept in departments:
        # อ่านไฟล์ที่ผ่านการแปลงมาตรฐานแล้ว
        filename = f"{dept}_full.json"
        if os.path.exists(filename):
            print(f"กำลังรวบรวมข้อมูลจาก {filename}...")
            with open(filename, "r", encoding="utf-8") as f:
                content = json.load(f)
                
                # จัดรูปแบบโครงสร้างข้อมูลให้เป็น List ภายในแต่ละกอง
                if isinstance(content, list):
                    all_materials[dept] = content
                elif isinstance(content, dict):
                    if dept in content and isinstance(content[dept], list):
                        all_materials[dept] = content[dept]
                    elif "products" in content and dept in content["products"]:
                        all_materials[dept] = content["products"][dept]
                    else:
                        # กรณีที่เป็น Dictionary ทั่วไป
                        for v in content.values():
                            if isinstance(v, list):
                                all_materials[dept] = v
                                break
        else:
            print(f"ไม่พบไฟล์ {filename}")

    payload = {"materials": all_materials}
    target_url = f"{FIREBASE_DB_URL.rstrip('/')}/.json"

    print("กำลังส่งข้อมูลมาตรฐานทั้งหมดขึ้น Firebase Realtime Database...")
    req = urllib.request.Request(
        target_url,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("อัปโหลดข้อมูลมาตรฐานขึ้น Firebase สำเร็จเรียบร้อยทุกกอง!")
            else:
                print(f"สถานะการตอบกลับ: {response.status}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    push_all_to_firebase()