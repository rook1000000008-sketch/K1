import os
import json
import urllib.request

FIREBASE_DB_URL = "https://kmart-cf668-default-rtdb.asia-southeast1.firebasedatabase.app/"

def process_items(dept, raw_items):
    standardized = []
    for index, item in enumerate(raw_items, start=1):
        # 1. จัดการ ID ให้เป็นรูปแบบมาตรฐาน เช่น 02fn_01
        item_id = str(item.get("id", f"{dept}_{index:02d}"))
        if not item_id.startswith(f"{dept}_"):
            item_id = f"{dept}_{int(item_id):02d}" if item_id.isdigit() else f"{dept}_{index:02d}"

        # 2. ชื่อวัสดุ (รองรับทั้ง name_th และ material_name)[cite: 8, 9]
        name = item.get("name_th") or item.get("material_name") or "ไม่ระบุชื่อ"

        # 3. จำนวนและราคา (แปลงเป็นตัวเลขเพื่อความถูกต้องในการคำนวณ)
        try:
            qty = int(item.get("quantity", 0))
        except:
            qty = 0

        try:
            price = float(item.get("unit_price", 0.0))
        except:
            price = 0.0

        unit = item.get("unit", "อัน")
        category = item.get("category", "วัสดุสำนักงาน")

        # 4. จัดการรูปภาพ (แปลง image_file หรือแก้ลิงก์เก่า BOSS เป็น K1)[cite: 8, 9, 11]
        img_url = item.get("image_url", "")
        img_file = item.get("image_file", "")

        if img_file:
            # ถ้ามีแค่ชื่อไฟล์ ให้สร้างลิงก์ CDN ของ K1
            img_url = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/{dept}/{img_file}"
        elif img_url:
            # ถ้ามีลิงก์เก่า ให้บังคับเปลี่ยนจาก BOSS เป็น K1
            img_url = img_url.replace("BOSS@main", "K1@main")
        
        if not img_url:
            img_url = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/{dept}/{dept}_{index:02d}.jpg"

        standardized.append({
            "id": item_id,
            "name_th": name,
            "quantity": qty,
            "unit": unit,
            "unit_price": price,
            "category": category,
            "image_url": img_url
        })
    return standardized

def main():
    departments = ["01sp", "02fn", "03en", "04ed", "05sw", "06ph"]
    all_materials = {}

    for dept in departments:
        filename = f"{dept}_full_2.json"
        if not os.path.exists(filename):
            filename = f"{dept}_full.json"
            
        if os.path.exists(filename):
            print(f"กำลังประมวลผลกอง: {dept} จากไฟล์ {filename}")
            with open(filename, "r", encoding="utf-8") as f:
                content = json.load(f)
                
                raw_list = []
                if isinstance(content, list):
                    raw_list = content
                elif isinstance(content, dict):
                    if dept in content and isinstance(content[dept], list):
                        raw_list = content[dept]
                    elif "products" in content:
                        prods = content["products"]
                        if isinstance(prods, dict):
                            raw_list = prods.get(dept, list(prods.values())[0] if prods else [])
                        elif isinstance(prods, list):
                            raw_list = prods
                    else:
                        # ค้นหาค่าที่เป็น list ภายใน dictionary
                        for v in content.values():
                            if isinstance(v, list):
                                raw_list = v
                                break

                all_materials[dept] = process_items(dept, raw_list)
        else:
            print(f"ไม่พบไฟล์ข้อมูลของกอง {dept}")

    payload = {"materials": all_materials}
    
    # บันทึกไฟล์สำรองในเครื่อง
    with open("kmart_standardized_output.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("สร้างไฟล์กลางมาตรฐานสำเร็จ: kmart_standardized_output.json")

    # ส่งขึ้น Firebase
    target_url = f"{FIREBASE_DB_URL.rstrip('/')}/.json"
    print("กำลังอัปโหลดข้อมูลมาตรฐานขึ้น Firebase Realtime Database...")
    
    req = urllib.request.Request(
        target_url,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("อัปโหลดและจัดระเบียบข้อมูลทุกกองขึ้น Firebase สำเร็จเรียบร้อย!")
            else:
                print(f"สถานะการตอบกลับ: {response.status}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอัปโหลด: {e}")

if __name__ == "__main__":
    main()