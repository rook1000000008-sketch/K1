import json
import os
import urllib.request

FIREBASE_DB_URL = "https://kmart-cf668-default-rtdb.asia-southeast1.firebasedatabase.app/"

def standardize_files():
    departments = ["01sp", "02fn", "03en", "04ed", "05sw", "06ph"]
    all_standardized_data = {}

    for dept in departments:
        filename = f"{dept}_full.json"
        if not os.path.exists(filename):
            print(f"ไม่พบไฟล์ {filename}")
            continue

        with open(filename, "r", encoding="utf-8") as f:
            content = json.load(f)

        # แกะดึง raw list ออกมาจากโครงสร้างที่ต่างกันของแต่ละกอง
        raw_list = []
        if isinstance(content, list):
            raw_list = content
        elif isinstance(content, dict):
            if dept in content and isinstance(content[dept], list):
                raw_list = content[dept]
            elif "products" in content and dept in content["products"]:
                raw_list = content["products"][dept]
            else:
                for v in content.values():
                    if isinstance(v, list):
                        raw_list = v
                        break

        standardized_items = []
        for index, item in enumerate(raw_list, start=1):
            if not isinstance(item, dict):
                continue
            
            # กำหนดชื่อฟิลด์ให้เป็นมาตรฐานเดียวกันทั้งหมด
            name = item.get("name_th") or item.get("material_name") or "ไม่ระบุชื่อ"
            category = item.get("category", "วัสดุสำนักงาน")
            unit = item.get("unit", "อัน")
            
            try:
                qty = int(item.get("quantity", 0) or 0)
            except:
                qty = 0

            try:
                price = float(item.get("unit_price", 0.0) or 0.0)
            except:
                price = 0.0

            img_file = item.get("image_file", f"{dept}_{index:02d}.jpg")
            if not img_file:
                img_file = f"{dept}_{index:02d}.jpg"
                
            img_url = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/{dept}/{img_file}"

            standardized_items.append({
                "id": f"{dept}_{index:02d}",
                "name_th": name,
                "category": category,
                "quantity": qty,
                "unit": unit,
                "unit_price": price,
                "image_file": img_file,
                "image_url": img_url
            })

        # บันทึกไฟล์ทับด้วยโครงสร้าง List มาตรฐานเดียวกัน 100%
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(standardized_items, f, ensure_ascii=False, indent=2)
            
        all_standardized_data[dept] = standardized_items
        print(f"แปลงไฟล์ {filename} เป็นรูปแบบมาตรฐานเรียบร้อยแล้ว")

    # อัปโหลดขึ้น Firebase ทันที
    payload = {"materials": all_standardized_data}
    target_url = f"{FIREBASE_DB_URL.rstrip('/')}/.json"
    
    req = urllib.request.Request(
        target_url,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("อัปเดตข้อมูลมาตรฐานทั้งหมดขึ้น Firebase สำเร็จสมบูรณ์!")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอัปโหลด Firebase: {e}")

if __name__ == "__main__":
    standardize_files()