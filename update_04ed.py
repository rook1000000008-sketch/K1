import json
import os

def fix_04ed_images():
    filename = "04ed_full_2.json"
    if not os.path.exists(filename):
        filename = "04ed_full.json"
        
    if os.path.exists(filename):
        print(f"กำลังอ่านข้อมูลจากไฟล์ {filename}...")
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # ตรวจสอบโครงสร้างข้อมูลของกองการศึกษาฯ (อยู่ที่ products.04ed)
        products_list = []
        if isinstance(data, dict):
            if "products" in data and "04ed" in data["products"]:
                products_list = data["products"]["04ed"]
            elif "04ed" in data:
                products_list = data["04ed"]
        elif isinstance(data, list):
            products_list = data

        for item in products_list:
            img_url = item.get("image_url", "")
            if img_url:
                # ดึงชื่อไฟล์จาก URL เดิม แล้วเปลี่ยนเส้นทางไปที่ K1@main/04ed/
                filename_img = img_url.split("/")[-1]
                item["image_url"] = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/04ed/{filename_img}"
            elif "image_file" in item:
                img_file = item["image_file"]
                item["image_url"] = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/04ed/{img_file}"

        # บันทึกไฟล์ผลลัพธ์
        with open("04ed_full.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("แปลงที่ตั้งภาพของกองการศึกษาฯ สำเร็จเรียบร้อย: 04ed_full.json")
    else:
        print("ไม่พบไฟล์ข้อมูลกองการศึกษาฯ ในระบบ")

if __name__ == "__main__":
    fix_04ed_images()