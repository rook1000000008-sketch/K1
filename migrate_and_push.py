import json
import urllib.request

# ตั้งค่า URL ของ Firebase Realtime Database ของคุณที่นี่
FIREBASE_DB_URL = "https://kmart-cf668-default-rtdb.asia-southeast1.firebasedatabase.app/"
GITHUB_USER = "rook1000000008-sketch"  # ชื่อยูสเซอร์ GitHub ของคุณ
REPO_NAME = "K1"                        # ชื่อ Repository ใหม่

def process_and_push_data():
    input_file = "kmart-cf668-export.json" # ชื่อไฟล์ JSON ต้นทางของคุณ
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ไม่พบไฟล์ {input_file} กรุณานำไฟล์ JSON มาวางไว้ในโฟลเดอร์ K1 ก่อนครับ")
        return

    materials = data.get("materials", {})
    
    for dept_key, dept_content in materials.items():
        products_list = []
        
        # จัดการโครงสร้างข้อมูลแยกตามรูปแบบของแต่ละกอง
        if isinstance(dept_content, dict):
            prods_dict = dept_content.get("products", {})
            if dept_key in prods_dict:
                products_list = prods_dict[dept_key]
            elif isinstance(prods_dict, dict) and len(prods_dict) > 0:
                products_list = list(prods_dict.values())[0]
        elif isinstance(dept_content, list):
            products_list = dept_content

        normalized_products = []
        for idx, item in enumerate(products_list, start=1):
            # ดึงชื่อวัสดุไม่ว่าจะมาจาก key ไหน
            name = item.get("name_th") or item.get("material_name") or "ไม่ระบุชื่อ"
            
            # ดึงราคาหน่วย
            price = item.get("unit_price") or item.get("price_unit_coin") or 0
            
            # ดึงจำนวน
            qty = item.get("quantity") or item.get("stock_remaining") or 0
            
            # จัดการลิงก์รูปภาพให้ชี้ไปที่ GitHub Repository ใหม่ "K1"
            img_url = item.get("image_url", "")
            img_file = item.get("image_file", "")
            
            if not img_url and img_file:
                img_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/products/{dept_key}/{img_file}"
            elif img_url and "BOSS@main" in img_url:
                # แทนที่ Repository เก่า (BOSS) ให้เป็นชื่อใหม่ (K1)
                img_url = img_url.replace("BOSS@main", f"{REPO_NAME}@main")

            item_id = item.get("id") or f"{dept_key}_{idx:02d}"

            # สร้างโครงสร้างมาตรฐานเดียวกันทุกรายการ
            normalized_item = {
                "id": item_id,
                "name_th": name,
                "quantity": str(qty),
                "unit": item.get("unit", "อัน"),
                "unit_price": float(price),
                "image_url": img_url,
                "category": item.get("category", "วัสดุสำนักงาน")
            }
            normalized_products.append(normalized_item)

        # บันทึกข้อมูลที่แปลงแล้วกลับลงไปในโครงสร้าง
        if isinstance(dept_content, dict):
            if dept_key in dept_content.get("products", {}):
                dept_content["products"][dept_key] = normalized_products
            else:
                first_key = list(dept_content.get("products", {}).keys())[0] if dept_content.get("products") else dept_key
                dept_content["products"][first_key] = normalized_products
        else:
            materials[dept_key] = normalized_products

    # เตรียมส่งข้อมูลขึ้น Firebase Realtime Database ผ่านคำสั่ง PUT ทีเดียวจบ
    push_data = {"materials": materials}
    target_url = f"{FIREBASE_DB_URL.rstrip('/')}/.json"
    
    print("กำลังส่งข้อมูลทั้งหมดขึ้น Firebase Realtime Database...")
    req = urllib.request.Request(
        target_url, 
        data=json.dumps(push_data, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("นำเข้าและปรับมาตรฐานข้อมูลพัสดุขึ้น Firebase สำเร็จเรียบร้อยแล้ว!")
            else:
                print(f"การอัปโหลดตอบสนองด้วยสถานะ: {response.status}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ Firebase: {e}")

if __name__ == "__main__":
    process_and_push_data()