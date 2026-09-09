import json
import os

# กำหนดเส้นทางโฟลเดอร์หลัก
base_dir = r"D:\K1"

# รายการชื่อไฟล์ JSON ของทั้ง 6 กอง (ปรับชื่อตามจริงที่คุณใช้งาน)
json_files = [
    "01sp_full.json",
    "02fn_full.json",
    "03en_full.json",
    "04ed_full.json",
    "05sw_full.json",
    "06ph_full.json",
]


def determine_category(item_name):
  """ฟังก์ชันสำหรับแยกประเภทวัสดุอย่างแม่นยำจากชื่อภาษาไทย"""
  name = str(item_name).lower()

  # คำค้นหาสำหรับวัสดุคอมพิวเตอร์ (หมึกพิมพ์, โทนเนอร์, คีย์บอร์ด, เมาส์, แฟลชไดรฟ์, ฯลฯ)
  computer_keywords = [
      "หมึก",
      "toner",
      "cartridge",
      "canon",
      "brother",
      "epson",
      "hp",
      "keyboard",
      "mouse",
      "เม้าส์",
      "คีย์บอร์ด",
      "แป้นพิมพ์",
      "แฟลชไดร์",
      "flash drive",
      "usb",
  ]

  for kw in computer_keywords:
    if kw in name:
      return "วัสดุคอมพิวเตอร์"

  # นอกเหนือจากนี้จัดเป็นวัสดุสำนักงาน
  return "วัสดุสำนักงาน"


def process_json_files():
  for filename in json_files:
    file_path = os.path.join(base_dir, filename)

    if not os.path.exists(file_path):
      print(f"⚠️ ไม่พบไฟล์: {file_path}")
      continue

    print(f"กำลังประมวลผลไฟล์: {filename}...")

    with open(file_path, "r", encoding="utf-8") as f:
      try:
        data = json.load(f)
      except Exception as e:
        print(f"❌ อ่านไฟล์ {filename} ไม่สำเร็จ: {e}")
        continue

    # ตรวจสอบโครงสร้างข้อมูล (รองรับทั้งแบบที่เป็น List ตรงๆ หรือ Object ที่มี Key เป็นชื่อกอง)
    updated = False
    if isinstance(data, list):
      for item in data:
        name_th = item.get("name_th", "")
        # กำหนด category ใหม่หรืออัปเดตให้แม่นยำ
        item["category"] = determine_category(name_th)
        updated = True
    elif isinstance(data, dict):
      for key, val in data.items():
        if isinstance(val, list):
          for item in val:
            name_th = item.get("name_th", "")
            item["category"] = determine_category(name_th)
            updated = True

    # บันทึกไฟล์กลับที่เดิม (เขียนทับด้วยรูปแบบที่จัดระเบียบสวยงาม)
    if updated:
      with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
      print(f"✅ อัปเดตและบันทึกไฟล์ {filename} สำเร็จเรียบร้อย!")


if __name__ == "__main__":
  process_json_files()