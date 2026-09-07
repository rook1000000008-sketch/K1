import os
import json
import urllib.request

FIREBASE_DB_URL = "https://kmart-cf668-default-rtdb.asia-southeast1.firebasedatabase.app/"
GITHUB_USER = "rook1000000008-sketch"
REPO_NAME = "K1"

def update_image_links():
    input_file = "kmart-cf668-export.json"
    
    if not os.path.exists(input_file):
        print(f"ไม่พบไฟล์ {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    materials = data.get("materials", {})

    for dept_key, dept_content in materials.items():
        products_list = []
        
        # จัดการโครงสร้างข้อมูลแต่ละกอง
        if isinstance(dept_content, dict):
            prods_dict = dept_content.get("products", {})
            if dept_key in prods_dict:
                products_list = prods_dict[dept_key]
            elif isinstance(prods_dict, dict) and len(prods_dict) > 0:
                products_list = list(prods_dict.values())[0]
        elif isinstance(dept_content, list):
            products_list = dept_content

        # ตรวจสอบไฟล์ที่มีจริงในโฟลเดอร์กองนั้นๆ (เช่น โฟลเดอร์ 01sp)
        dept_folder = dept_key
        existing_files = []
        if os.path.exists(dept_folder) and os.path.isdir(dept_folder):
            existing_files = os.listdir(dept_folder)

        for idx, item in enumerate(products_list, start=1):
            item_id = str(item.get("id") or f"{dept_key}_{idx:02d}")
            
            # ค้นหาไฟล์ในโฟลเดอร์ที่ขึ้นต้นด้วยรหัสสินค้า เช่น "01sp_01"
            matched_file = ""
            for filename in existing_files:
                if filename.startswith(item_id):
                    matched_file = filename
                    break

            # ถ้าเจอไฟล์ในเครื่อง ให้สร้างลิงก์ GitHub K1 ทันที
            if matched_file:
                img_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{dept_key}/{matched_file}"
                item["image_url"] = img_url
                item["image_file"] = matched_file
            else:
                # ถ้าไม่พบไฟล์ในเครื่อง ให้ตรวจสอบลิงก์เดิมและเปลี่ยนเป็น K1 หากจำเป็น
                old_url = item.get("image_url", "")
                if old_url:
                    if "BOSS@main" in old_url:
                        item["image_url"] = old_url.replace("BOSS@main", f"{REPO_NAME}@main")
                elif item.get("image_file"):
                    img_file = item.get("image_file")
                    item["image_url"] = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{dept_key}/{img_file}"

            # รักษามาตรฐานชื่อฟิลด์ข้อมูล
            if "material_name" in item and "name_th" not in item:
                item["name_th"] = item["material_name"]
            if "unit_price" in item and "unit_price" not in item:
                item["unit_price"] = float(item["unit_price"])

        # บันทึกข้อมูลที่จับคู่รูปภาพแล้วกลับเข้าโครงสร้างเดิม
        if isinstance(dept_content, dict):
            if dept_key in dept_content.get("products", {}):
                dept_content["products"][dept_key] = products_list
            else:
                first_key = list(dept_content.get("products", {}).keys())[0] if dept_content.get("products") else dept_key
                dept_content["products"][first_key] = products_list
        else:
            materials[dept_key] = products_list

    # ส่งข้อมูลที่อัปเดตลิงก์รูปภาพครบถ้วนแล้วขึ้น Firebase
    push_data = {"materials": materials}
    target_url = f"{FIREBASE_DB_URL.rstrip('/')}/.json"
    
    print("กำลังอัปเดตลิงก์รูปภาพทั้งหมดขึ้น Firebase Realtime Database...")
    req = urllib.request.Request(
        target_url, 
        data=json.dumps(push_data, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("อัปเดตลิงก์รูปภาพทุกกองสำเร็จเรียบร้อยแล้ว!")
            else:
                print(f"สถานะการตอบกลับ: {response.status}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    update_image_links()