import os
import json
import urllib.request

FIREBASE_DB_URL = "https://kmart-cf668-default-rtdb.asia-southeast1.firebasedatabase.app/"

def push_all_departments():
    departments = ["01sp", "02fn", "03en", "04ed", "05sw", "06ph"]
    all_materials = {}

    for dept in departments:
        filename = f"{dept}_full.json"
        if os.path.exists(filename):
            print(f"กำลังอ่านข้อมูลจากไฟล์ {filename}...")
            with open(filename, "r", encoding="utf-8") as f:
                content = json.load(f)
                
                # จัดรูปแบบโครงสร้างข้อมูลให้อยู่ในรูปแบบมาตราฐานเดียวกัน
                if isinstance(content, dict):
                    if dept in content:
                        all_materials[dept] = content[dept]
                    elif "products" in content:
                        prods = content["products"]
                        if isinstance(prods, dict):
                            all_materials[dept] = prods.get(dept, list(prods.values())[0] if prods else [])
                        elif isinstance(prods, list):
                            all_materials[dept] = prods
                    else:
                        # กรณีไฟล์ 01sp_full.json ที่มีโครงสร้างตรง
                        for k, v in content.items():
                            all_materials[k] = v
                elif isinstance(content, list):
                    all_materials[dept] = content
        else:
            print(f"ไม่พบไฟล์ {filename} ข้ามการอัปโหลดของกองนี้")

    # รวมข้อมูลทุกกองเข้าสู่โครงสร้างหลัก
    payload = {"materials": all_materials}
    target_url = f"{FIREBASE_DB_URL.rstrip('/')}/.json"

    print("กำลังส่งข้อมูลทั้งหมดขึ้น Firebase Realtime Database...")
    req = urllib.request.Request(
        target_url,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("อัปเดตแทนที่ข้อมูลทั้ง 6 กองบน Firebase สำเร็จเรียบร้อยแล้ว!")
            else:
                print(f"สถานะการตอบกลับ: {response.status}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    push_all_departments()