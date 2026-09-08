import json
import os

def fix_05sw_images():
    filename = "05sw_full_2.json"
    if not os.path.exists(filename):
        filename = "05sw_full.json"
        
    if os.path.exists(filename):
        print(f"กำลังอ่านข้อมูลจากไฟล์ {filename}...")
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # รองรับโครงสร้างทั้งแบบมี products.05sw หรือเป็น list โดยตรง[cite: 12]
        products_list = []
        if isinstance(data, dict):
            if "products" in data and "05sw" in data["products"]:
                products_list = data["products"]["05sw"]
            elif "05sw" in data:
                products_list = data["05sw"]
        elif isinstance(data, list):
            products_list = data

        for item in products_list:
            img_url = item.get("image_url", "")
            if img_url:
                filename_img = img_url.split("/")[-1]
                item["image_url"] = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/05sw/{filename_img}"
            elif "image_file" in item:
                img_file = item["image_file"]
                item["image_url"] = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/05sw/{img_file}"

        with open("05sw_full.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("แปลงที่ตั้งภาพของกองสวัสดิการสังคมสำเร็จเรียบร้อย: 05sw_full.json")
    else:
        print("ไม่พบไฟล์ข้อมูลกองสวัสดิการสังคมในระบบ")

if __name__ == "__main__":
    fix_05sw_images()