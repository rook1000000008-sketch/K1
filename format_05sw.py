import json
import os

file_path = r"D:\K1\05sw_full.json"
base_url = "https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/05sw/"


def determine_category(item_name):
  name = str(item_name).lower()
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
  return "วัสดุสำนักงาน"


if os.path.exists(file_path):
  with open(file_path, "r", encoding="utf-8") as f:
    text_data = f.read()

  # แก้ไขโครงสร้างวงเล็บปีกกาที่ซ้อนกันผิดพลาดให้อัตโนมัติ
  text_data = text_data.strip()
  if text_data.startswith("{\n    {") or text_data.startswith("{    {"):
    # แปลงโครงสร้างภายในให้เป็นรูปแบบ List มาตรฐาน
    text_data = "[" + text_data[1:]
    if text_data.endswith("}"):
      text_data = text_data[:-1] + "]"

  try:
    items_list = json.loads(text_data)
  except Exception as e:
    # หากยังติดปัญหา ให้ดึงข้อมูลเฉพาะส่วนที่เป็น Object ด้านในมาทำเป็น List
    import re

    objects = re.findall(r"\{\s*\"id\".*?\}", text_data, re.DOTALL)
    items_list = [json.loads(obj) for obj in objects]

  formatted_items = []
  for item in items_list:
    original_url = item.get("image_url", "")
    image_file = (
        original_url.split("/")[-1]
        if original_url
        else f"{item.get('id')}.jpg"
    )
    name_th = item.get("name_th", "")

    new_item = {
        "id": item.get("id"),
        "name_th": name_th,
        "category": determine_category(name_th),
        "quantity": int(item.get("quantity", 0)),
        "unit": item.get("unit"),
        "unit_price": float(item.get("unit_price", 0.0)),
        "image_file": image_file,
        "image_url": base_url + image_file,
    }
    formatted_items.append(new_item)

  with open(file_path, "w", encoding="utf-8") as f:
    json.dump(formatted_items, f, ensure_ascii=False, indent=2)

  print(
      "✅ แก้ไขโครงสร้างและจัดรูปแบบข้อมูลของ 05sw_full.json เรียบร้อยแล้วครับ!"
  )
else:
  print(f"❌ ไม่พบไฟล์: {file_path}")