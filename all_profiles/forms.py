# hoso/forms.py

from django import forms
from .models import HoSo

class HoSoForm(forms.ModelForm):
    class Meta:
        model = HoSo
        fields = '__all__'  # hoặc liệt kê cụ thể: ['dot_nhap', 'db_cu', 'hd_cu', ...]
        labels = {
            'so_ho_so': 'SỐ HỒ SƠ',
            'bang_ke_dot_gan': 'BẢNG KÊ ĐỢT GẮN',
            'dot_nhap': 'ĐỢT NHẬP',
            'db_cu': 'DANH BẠ CŨ',
            'hd_cu': 'HỢP ĐỒNG CŨ',
            'db_moi': 'DANH BẠ MỚI',
            'hd_moi': 'HỢP ĐỒNG MỚI',
            'dot': 'ĐỢT',
            'gb': 'GIÁ BIỂU',
            'bu_dm': 'BÙ ĐỊNH MỨC',
            'hieu_luc': 'HIỆU LỰC',
            'ma_hd': 'MÃ HỢP ĐỒNG',
            'ds_luu': 'DS LƯU',
            'ghi_chu': 'GHI CHÚ',
            'tro_ngai': 'TRỞ NGẠI',
            'quan': 'QUẬN',
            'lan_nhap': 'LẦN NHẬP',
        }