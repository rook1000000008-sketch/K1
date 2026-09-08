import json
import urllib.request
import os

FIREBASE_DB_URL = "https://kmart-cf668-default-rtdb.asia-southeast1.firebasedatabase.app/"

def migrate_data():
    departments_map = {
        "01sp": "สำนักปลัด",
        "02fn": "กองคลัง",
        "03en": "กองช่าง",
        "04ed": "กองการศึกษา ศาสนา และวัฒนธรรม",
        "05sw": "กองสวัสดิการสังคม",
        "06ph": "กองสาธารณสุขและสิ่งแวดล้อม"
    }

    target_url = f"{FIREBASE_DB_URL.rstrip('/')}/kmart_data.json"
    print("กำลังดึงข้อมูลโครงสร้างจาก Firebase...")
    try:
        req = urllib.request.Request(target_url, method='GET')
        with urllib.request.urlopen(req) as response:
            cloud_data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print("ยังไม่มีข้อมูลบน Firebase หรือเกิดข้อผิดพลาด ใช้โครงสร้างเริ่มต้น")
        cloud_data = None

    if not cloud_data or "divisions" not in cloud_data:
        print("กรุณารันระบบผ่าน index.html ครั้งแรกก่อนเพื่อให้ Firebase สร้างโครงสร้าง divisions พื้นฐาน")
        return

    for folder_code, div_name in departments_map.items():
        filename = f"{folder_code}_full.json"
        if os.path.exists(filename):
            print(f"กำลังอ่านและแปลงข้อมูลของ: {div_name} ({filename})")
            with open(filename, "r", encoding="utf-8") as f:
                items = json.load(f)
            
            formatted_materials = []
            for i, item in enumerate(items, start=1):
                # ตรวจสอบว่า item เป็น dict หรือ str เพื่อป้องกัน Error
                if isinstance(item, dict):
                    name = item.get("name_th") or item.get("material_name") or "ไม่ระบุชื่อ"
                    try:
                        qty = int(item.get("quantity", 10) or 10)
                    except:
                        qty = 10

                    try:
                        price = float(item.get("unit_price", 100.0) or 100.0)
                    except:
                        price = 100.0

                    img_file = item.get("image_file", "")
                    img_url = item.get("image_url", "")
                    if img_file:
                        img_url = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/{folder_code}/{img_file}"
                    elif not img_url:
                        img_url = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/{folder_code}/{folder_code}_{i:02d}.jpg"
                else:
                    # กรณีที่ item เป็นสตริงธรรมดา
                    name = str(item)
                    qty = 10
                    price = 100.0
                    img_url = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/{folder_code}/{folder_code}_{i:02d}.jpg"

                formatted_materials.append({
                    "item_id": f"KP-ITEM-{folder_code}-{i:02d}",
                    "item_name": name,
                    "type": "office",
                    "price_unit_coin": price,
                    "stock_remaining": qty,
                    "fifo_date": "2026-08-23",
                    "image_url": img_url,
                    "owner_division": div_name
                })
            
            if div_name in cloud_data["divisions"]:
                cloud_data["divisions"][div_name]["materials"] = formatted_materials

    print("กำลังอัปโหลดข้อมูลทั้งหมดขึ้น Firebase (kmart_data)...")
    put_req = urllib.request.Request(
        target_url,
        data=json.dumps(cloud_data, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    try:
        with urllib.request.urlopen(put_req) as response:
            if response.status == 200:
                print("ย้ายข้อมูลและอัปเดตขึ้น Firebase สำเร็จสมบูรณ์ทุกกอง!")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    migrate_data()