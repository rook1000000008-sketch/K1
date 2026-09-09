import json
import urllib.request
import os

FIREBASE_DB_URL = "https://kmart-cf668-default-rtdb.asia-southeast1.firebasedatabase.app/"

# รายชื่อไฟล์ภาพจริงของกองคลังที่คุณให้มา
exact_files_02fn = [
    "02fn_01_gem_paper_clip_no1.jpg",
    "02fn_02_gem_paper_clip_no0.jpg",
    "02fn_03_correction_tape.jpg",
    "02fn_04_clear_tape.jpg",
    "02fn_05_blue_permanent_marker.jpg",
    "02fn_06_red_ballpoint_pen.jpg",
    "02fn_07_black_ballpoint_pen.jpg",
    "02fn_08_eraser.jpg",
    "02fn_09_binding_spine_5mm.jpg",
    "02fn_10_large_cloth_tape.jpg",
    "02fn_11_binder_clip_no108.jpg",
    "02fn_12_red_stamp_pad_no2.jpg",
    "02fn_13_blue_stamp_pad_no2.jpg",
    "02fn_14_binder_clip_no112.jpg",
    "02fn_15_assorted_highlighters.jpg",
    "02fn_16_thin_double_sided_tape.jpg",
    "02fn_17_staples_no10_1m.jpg",
    "02fn_18_staples_nom8_1m.jpg",
    "02fn_19_large_cutter_knife.jpg",
    "02fn_20_blue_stamp_ink.jpg",
    "02fn_21_red_stamp_ink.jpg",
    "02fn_22_large_scissors.jpg",
    "02fn_23_matte_white_sticker_paper.jpg",
    "02fn_24_glossy_white_sticker_paper.jpg",
    "02fn_25_photo_paper.jpg",
    "02fn_26_envelopes.jpg",
    "02fn_27_expansion_kraft_envelope.jpg",
    "02fn_28_standard_kraft_envelope.jpg",
    "02fn_29_hard_paper.jpg",
    "02fn_30_aa_batteries.jpg",
    "02fn_31_contract_guarantee_register.jpg",
    "02fn_32_durable_goods_register.jpg",
    "02fn_33_land_and_building_registry.jpg",
    "02fn_34_blue_ballpoint_pen_box.jpg",
    "02fn_35_crepe_masking_tape.jpg",
    "02fn_36_hole_punch.jpg",
    "02fn_37_calculator.jpg",
    "02fn_38_paint_marker.jpg",
    "02fn_39_staple_remover.jpg",
    "02fn_40_extension_cord_5m.jpg",
    "02fn_41_laminating_pouch_film.jpg",
    "02fn_42_aaa_batteries.jpg",
    "02fn_43_sticky_notes.jpg",
    "02fn_44_white_card_paper_150gsm.jpg",
    "02fn_45_foam_tape_21mm.jpg",
    "02fn_46_extension_cord_10m.jpg",
    "02fn_47_canon_325_toner.jpg",
    "02fn_48_brother_tn2480_toner.jpg",
    "02fn_49_hp_30a_toner.jpg",
    "02fn_50_brother_tn2360_toner.jpg",
    "02fn_51_keyboard_mouse_usb.jpg",
    "02fn_52_flash_drive.jpg",
    "02fn_53_epson_003_bk_ink.jpg",
    "02fn_54_brother_tn267_black.jpg",
    "02fn_55_brother_tn267_magenta.jpg",
    "02fn_56_brother_tn267_yellow.jpg",
    "02fn_57_brother_tn267_cyan.jpg",
    "02fn_58_hp_12a_toner.jpg"
]

def update_and_push_02fn():
    # 1. โหลดข้อมูลเดิมทั้งหมดจาก Firebase หรือจากไฟล์กลาง
    target_url = f"{FIREBASE_DB_URL.rstrip('/')}/.json"
    print("กำลังดึงข้อมูลปัจจุบันจาก Firebase...")
    
    try:
        req = urllib.request.Request(target_url, method='GET')
        with urllib.request.urlopen(req) as response:
            db_data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการดึงข้อมูล: {e}")
        return

    if not db_data or "materials" not in db_data or "02fn" not in db_data["materials"]:
        print("ไม่พบข้อมูลโครงสร้างของกองคลังใน Firebase")
        return

    items_02fn = db_data["materials"]["02fn"]

    # 2. อัปเดต image_url ให้ตรงกับรายชื่อไฟล์จริงเป๊ะๆ
    for i, item in enumerate(items_02fn):
        if i < len(exact_files_02fn):
            filename = exact_files_02fn[i]
            item["image_url"] = f"https://cdn.jsdelivr.02fn_filename_fix.../gh/rook1000000008-sketch/K1@main/02fn/{filename}".replace("jsdelivr.02fn_filename_fix...", "jsdelivr.net")
            # หรือเขียนตรงๆ แบบนี้ครับ:
            item["image_url"] = f"https://cdn.jsdelivr.net/gh/rook1000000008-sketch/K1@main/02fn/{filename}"
        
        # ปรับชื่อฟิลด์ให้ได้มาตรฐาน (รองรับ name_th)
        if "material_name" in item and "name_th" not in item:
            item["name_th"] = item["material_name"]

    # บันทึกทับลง Firebase (อัปเดตเฉพาะคีย์ 02fn หรืออัปเดตทั้งก้อน)
    db_data["materials"]["02fn"] = items_02fn

    print("กำลังอัปเดตข้อมูลกองคลังที่แก้ไขชื่อภาพแล้วขึ้น Firebase...")
    put_req = urllib.request.Request(
        target_url,
        data=json.dumps(db_data, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    try:
        with urllib.request.urlopen(put_req) as response:
            if response.status == 200:
                print("อัปเดตภาพกองคลังสำเร็จสมบูรณ์ทุกรายการ!")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอัปโหลด: {e}")

if __name__ == "__main__":
    update_and_push_02fn()