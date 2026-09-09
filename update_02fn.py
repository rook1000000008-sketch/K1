import json
import os

def fix_02fn_images():
    # ค้นหาไฟล์ข้อมูลของกองคลัง
    filename = "02fn_full_2.json"
    if not os.path.exists(filename):
        filename = "02fn_full.json"
        
    if os.path.exists(filename):
        print(f"กำลังอ่านข้อมูลจากไฟล์ {filename}...")
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # กองคลังมีโครงสร้างเป็น List ของสินค้า[cite: 9]
        items = data if isinstance(data, list) else data.get("02fn", [])
        
        updated_items = []
        for item in items:
            img_file = item.get("image_file", "")
            
            # ถ้ามี image_file แต่ยังไม่มี image_url ให้สร้างลิงก์ CDN เต็มรูปแบบ
            if img_file:
                item["image_url"] = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/02fn/{img_file}"
            
            updated_items.append(item)
            
        # บันทึกไฟล์ทับหรือสร้างไฟล์ใหม่
        with open("02fn_full.json", "w", encoding="utf-8") as f:
            json.dump(updated_items, f, ensure_ascii=False, indent=2)
            
        print("แปลงที่ตั้งภาพของกองคลังสำเร็จเรียบร้อย: 02fn_full.json")
    else:
        print(f"ไม่พบไฟล์ข้อมูลกองคลังในระบบ")

if __name__ == "__main__":
    fix_02fn_images()