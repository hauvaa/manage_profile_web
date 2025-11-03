import os
import django
import pandas as pd
import numpy as np

# Thiết lập Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # <-- Đổi thành tên project của bạn
django.setup()

from all_profiles.models import HoSo  # <-- Đổi thành tên app chứa model HoSo

# Đường dẫn tới file Excel
excel_file_path = "Book1.xlsx"  # <-- Thay bằng đường dẫn tới file Excel của bạn

# Đọc file Excel
df = pd.read_excel(
    excel_file_path,
    dtype={
        'db_cu': str,
        'db_moi': str,
        'bu_dm': str,
        'ma_hd': str
    }
)

# Xóa sạch dữ liệu cũ
HoSo.objects.all().delete()
print("🧹 Đã xóa toàn bộ dữ liệu cũ.")

# Hàm làm sạch giá trị chuỗi (None nếu rỗng hoặc NaN)
def clean_value(val):
    if pd.isna(val) or (isinstance(val, str) and val.strip() == ''):
        return None
    # Nếu là số float nhưng thực chất là số nguyên => bỏ .0
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val).strip()


# Lặp qua từng dòng để tạo bản ghi HoSo
for _, row in df.iterrows():
    try:
        HoSo.objects.update_or_create(
            so_ho_so=row['so_ho_so'],
            defaults={
                'bang_ke_dot_gan': clean_value(row.get('bang_ke_dot_gan')),
                'dot_nhap': clean_value(row.get('dot_nhap')),
                'db_cu': clean_value(row.get('db_cu')),
                'hd_cu': clean_value(row.get('hd_cu')),
                'db_moi': clean_value(row.get('db_moi')),
                'hd_moi': clean_value(row.get('hd_moi')),
                'dot': clean_value(row.get('dot')),
                'gb': clean_value(row.get('gb')),
                'bu_dm': clean_value(row.get('bu_dm')),
                'hieu_luc': clean_value(row.get('hieu_luc')),
                'ma_hd': clean_value(row.get('ma_hd')),
                'ds_luu': clean_value(row.get('ds_luu')),
                'ghi_chu': clean_value(row.get('ghi_chu')),
                'tro_ngai': clean_value(row.get('tro_ngai')),
                'quan': clean_value(row.get('quan')),
                'lan_nhap': clean_value(row.get('lan_nhap')),
            }
        )
        print(f"✅ Imported: {row['so_ho_so']}")
    except Exception as e:
        print(f"❌ Lỗi khi import hồ sơ {row['so_ho_so']}: {e}")
