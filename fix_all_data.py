import os
import json
import urllib.request

FIREBASE_DB_URL = "https://kmart-cf668-default-rtdb.asia-southeast1.firebasedatabase.app/"

def standardize_department(dept, raw_items):
    standardized = []
    for index, item in enumerate(raw_items, start=1):
        item_id = str(item.get("id", f"{dept}_{index:02d}"))
        if not item_id.startswith(f"{dept}_"):
            item_id = f"{dept}_{index:02d}"

        name = item.get("name_th") or item.get("material_name") or "ไม่ระบุชื่อ"
        
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

        # จัดการรูปภาพ แก้ลิงก์ BOSS เป็น K1 และรองรับทั้ง jpg / png
        img_url = item.get("image_url", "")
        img_file = item.get("image_file", "")

        if img_file:
            img_url = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/{dept}/{img_file}"
        elif img_url:
            # แปลงลิงก์เก่าทุกรูปแบบให้เป็น K1@main
            img_url = img_url.replace("BOSS@main", "K1@main").replace("K1@main/products/", "K1@main/")
        
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
            print(f"กำลังประมวลผลกอง: {dept}")
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
                            raw_list = prods.get(dept, [])
                        elif isinstance(prods, list):
                            raw_list = prods
                    else:
                        for v in content.values():
                            if isinstance(v, list):
                                raw_list = v
                                break

                all_materials[dept] = standardize_department(dept, raw_list)

    payload = {"materials": all_materials}
    
    # อัปโหลดขึ้น Firebase
    target_url = f"{FIREBASE_DB_URL.rstrip('/')}/.json"
    print("กำลังอัปโหลดข้อมูลมาตรฐานขึ้น Firebase...")
    
    req = urllib.request.Request(
        target_url,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("อัปเดตข้อมูลสำเร็จเรียบร้อยทุกกอง!")
            else:
                print(f"สถานะ: {response.status}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()