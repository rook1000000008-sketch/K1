import json
import os

def fix_03en_images():
    filename = "03en_full_2.json"
    if not os.path.exists(filename):
        filename = "03en_full.json"
        
    if os.path.exists(filename):
        print(f"กำลังอ่านข้อมูลจากไฟล์ {filename}...")
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        items = data if isinstance(data, list) else data.get("03en", [])
        
        updated_items = []
        for item in items:
            img_file = item.get("image_file", "")
            
            if img_file:
                item["image_url"] = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/03en/{img_file}"
            
            updated_items.append(item)
            
        with open("03en_full.json", "w", encoding="utf-8") as f:
            json.dump(updated_items, f, ensure_ascii=False, indent=2)
            
        print("แปลงที่ตั้งภาพของกองช่างสำเร็จเรียบร้อย: 03en_full.json")
    else:
        print("ไม่พบไฟล์ข้อมูลกองช่างในระบบ")

if __name__ == "__main__":
    fix_03en_images()