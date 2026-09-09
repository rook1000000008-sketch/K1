import json
import os

# กำหนดเส้นทางไฟล์
json_file_path = r"D:\K1\04ed_full.json"  # ปรับ path ตามตำแหน่งไฟล์จริงของคุณ
base_url = "https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/04ed/"

# รายการชื่อไฟล์ภาพจริงในโฟลเดอร์ (เรียงตามลำดับ 01 ถึง 28)
image_files = [
    "04ed_01_grey_book_paper.png",
    "04ed_02_wide_spine_file_size_3_inches.png",
    "04ed_03_wide_spine_file_size_1_inch.png",
    "04ed_04_board_wire_t3-13mb.png",
    "04ed_05_a4_paper_size_80_grams.png",
    "04ed_06_photo_paper_120_grams.png",
    "04ed_07_a4_white_matte_sticker_paper.png",
    "04ed_08_blue_ballpoint_pen_size_0.5_mm..png",
    "04ed_09_highlighter.png",
    "04ed_10_large_cutter_knife_no_st-20.png",
    "04ed_11_correction_tape.png",
    "04ed_12_scissors_size_8_inches.png",
    "04ed_13_stapler_number_10.png",
    "04ed_14_aa_alkaline_type_batteries.png",
    "04ed_15_aaa_alkaline_type_battery.png",
    "04ed_16_wire_for_paper_small.png",
    "04ed_17_wire_for_inserting_paper_large.png",
    "04ed_18_black_clip_2_legs_25_mm..png",
    "04ed_19_black_clip_2_legs_50_mm..png",
    "04ed_20_epson_l3110_printer_ink_red.png",
    "04ed_21_epson_l3110_printer_ink_blue.png",
    "04ed_22_epson_l3110_printer_ink_yellow.png",
    "04ed_23_printer_ink_brother_hl-l3270_yellow.png",
    "04ed_24_printer_ink_brother_hl-l3270_black.png",
    "04ed_25_printer_ink_brother_hl-l3270_red.png",
    "04ed_26_printer_ink_brother_hl-l3270_blue.png",
    "04ed_27_mouse_has_wires.png",
    "04ed_28_keyboard_and_mouse_set_usb_connection_type.png",
]

# โหลดข้อมูล JSON เดิม
if os.path.exists(json_file_path):
  with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
else:
  print(f"❌ ไม่พบไฟล์: {json_file_path}")
  data = []

updated_data = []

# วนลูปอัปเดตข้อมูลทีละรายการ
for index, item in enumerate(data):
  if index < len(image_files):
    img_filename = image_files[index]
  else:
    img_filename = f"04ed_{index+1:02d}.png"  # ค่าสำรองหากรายการเกิน

  # จัดเรียงโครงสร้างฟิลด์ใหม่ตามที่คุณต้องการ
  formatted_item = {
      "id": item.get("id"),
      "name_th": item.get("name_th"),
      "category": item.get("category"),
      "quantity": item.get("quantity"),
      "unit": item.get("unit"),
      "unit_price": item.get("unit_price", 0.0),
      "image_file": img_filename,
      "image_url": base_url + img_filename,
  }
  updated_data.append(formatted_item)

# บันทึกไฟล์ JSON กลับที่เดิม (จัดรูปแบบสวยงามและรองรับภาษาไทย)
with open(json_file_path, "w", encoding="utf-8") as f:
  json.dump(updated_data, f, ensure_ascii=False, indent=2)

print(
    "✅ อัปเดตชื่อไฟล์ภาพ ลิงก์ URL และจัดเรียงฟิลด์ในไฟล์ 04ed_full.json"
    " เรียบร้อยแล้วครับ!"
)