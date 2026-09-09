import json
import os

# แก้ชื่อไฟล์ให้ตรงกับชื่อจริงในแถบซ้าย (01sp_full.json)
file_path = r"D:\K1\01sp_full.json"
base_url = "https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/01sp/"

if os.path.exists(file_path):
  with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

  # ตรวจสอบโครงสร้างข้อมูล (รองรับทั้งแบบที่เป็น Dict ครอบด้วย Key และแบบ List)
  if isinstance(data, dict):
    root_key = list(data.keys())[0]
    items_list = data[root_key]
  else:
    items_list = data

  formatted_items = []
  for item in items_list:
    original_url = item.get("image_url", "")
    if original_url:
      image_file = original_url.split("/")[-1]
    else:
      image_file = f"{item.get('id')}.jpg"

    # จัดเรียงฟิลด์ใหม่ให้ตรงกับรูปแบบ 02fn
    new_item = {
        "id": item.get("id"),
        "name_th": item.get("name_th"),
        "category": item.get("category", "วัสดุสำนักงาน"),
        "quantity": int(
            item.get("quantity", 0)
        ),  # แปลง quantity เป็นตัวเลข
        "unit": item.get("unit"),
        "unit_price": float(item.get("unit_price", 0.0)),
        "image_file": image_file,
        "image_url": base_url + image_file,
    }
    formatted_items.append(new_item)

  # ประกอบโครงสร้างข้อมูลกลับคืนรูปแบบเดิม
  if isinstance(data, dict):
    data[root_key] = formatted_items
    output_data = data
  else:
    output_data = formatted_items

  # บันทึกทับไฟล์เดิม
  with open(file_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

  print("✅ ปรับรูปแบบข้อมูลของ 01sp เรียบร้อยแล้วครับ!")
else:
  print(f"❌ ไม่พบไฟล์: {file_path}")