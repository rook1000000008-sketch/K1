import json
import os

def fix_06ph_images():
    filename = "06ph_full_2.json"
    if not os.path.exists(filename):
        filename = "06ph_full.json"
        
    if os.path.exists(filename):
        print(f"กำลังอ่านข้อมูลจากไฟล์ {filename}...")
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # กองสาธารณสุขฯ มีโครงสร้างเป็น List[cite: 13] หรือ Dict
        products_list = []
        if isinstance(data, list):
            products_list = data
        elif isinstance(data, dict):
            if "06ph" in data and isinstance(data["06ph"], list):
                products_list = data["06ph"]
            else:
                for v in data.values():
                    if isinstance(v, list):
                        products_list = v
                        break

        for item in products_list:
            img_file = item.get("image_file", "")
            img_url = item.get("image_url", "")
            
            if img_file:
                item["image_url"] = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/06ph/{img_file}"
            elif img_url:
                filename_img = img_url.split("/")[-1]
                item["image_url"] = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/06ph/{filename_img}"

        # บันทึกไฟล์ผลลัพธ์
        with open("06ph_full.json", "w", encoding="utf-8") as f:
            json.dump(products_list, f, ensure_ascii=False, indent=2)
            
        print("แปลงที่ตั้งภาพของกองสาธารณสุขฯ สำเร็จเรียบร้อย: 06ph_full.json")
    else:
        print("ไม่พบไฟล์ข้อมูลกองสาธารณสุขฯ ในระบบ")

if __name__ == "__main__":
    fix_06ph_images()