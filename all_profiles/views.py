import re
from collections import defaultdict
from turtledemo.penrose import start

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import HoSo
from django.core.paginator import Paginator
from .forms import HoSoForm
from django.contrib import messages
from openpyxl import Workbook

def trang_chu(request):
    return render(request, 'main.html')

def tat_ca_ho_so(request):
    page_number = int(request.GET.get('page', 1))
    per_page = 500
    start_index = (page_number - 1) * per_page
    end_index = start_index + per_page

    # Chỉ lấy đúng 500 bản ghi từ DB
    ho_so_page = HoSo.objects.all()[start_index:end_index]

    # Đếm tổng số bản ghi để tính số trang
    total_ho_so = HoSo.objects.count()
    total_pages = (total_ho_so + per_page - 1) // per_page  # làm tròn lên

    # Tính STT bắt đầu
    ho_sos = list(enumerate(ho_so_page, start=start_index + 1))

    return render(request, 'tat_ca_ho_so.html', {
        'ho_sos': ho_sos,
        'current_page': page_number,
        'total_pages': total_pages,
    })

def search_hoso(request):
    search_field = request.GET.get('search_field')
    search_value = request.GET.get('search_value')
    page_number = int(request.GET.get('page', 1))
    per_page = 500
    start_index = (page_number - 1) * per_page
    end_index = start_index + per_page

    ket_qua = HoSo.objects.none()
    total_ket_qua = 0

    if search_field and search_value:
        if search_field == 'danh_ba':
            ket_qua_full = HoSo.objects.filter(
                Q(db_cu__icontains=search_value) | Q(db_moi__icontains=search_value)
            )
        elif search_field == 'hop_dong':
            ket_qua_full = HoSo.objects.filter(
                Q(hd_cu__icontains=search_value) | Q(hd_moi__icontains=search_value)
            )
        else:
            if search_field == 'ds_luu':
                try:
                    search_value_int = int(search_value)
                    ket_qua_full = HoSo.objects.filter(ds_luu=search_value_int)
                except ValueError:
                    ket_qua_full = HoSo.objects.none()  # Nếu người dùng nhập chuỗi không phải số
            else:
                filter_kwargs = {f"{search_field}__icontains": search_value}
                ket_qua_full = HoSo.objects.filter(**filter_kwargs)

    total_ket_qua = ket_qua_full.count()
    ket_qua = ket_qua_full[start_index:end_index]
    print(f"Tìm với {search_field} = '{search_value}'")
    print("Tổng kết quả:", ket_qua_full.count())

    total_pages = (total_ket_qua + per_page - 1) // per_page
    ho_sos = list(enumerate(ket_qua, start=start_index + 1))

    FIELD_LABELS = {
        'bang_ke_dot_gan': 'Bảng kê đợt gắn',
        'dot_nhap': 'Đợt nhập',
        'so_ho_so': 'Số hồ sơ',
        'danh_ba': 'Danh bạ',
        'hop_dong': 'Hợp đồng',
        'dot': 'Đợt',
        'hieu_luc': 'Hiệu lực',
        'ma_hop_dong': 'Mã hợp đồng',
        'ds_luu': 'DS lưu',
        'quan': 'Quận',
        'db_cu': 'DB cũ',
        'db_moi': 'DB mới',
        'hd_cu': 'HD cũ',
        'hd_moi': 'HD mới',
        # thêm nếu cần
    }

    # Trong context:
    context = {
        'ho_sos': ho_sos,
        'current_page': page_number,
        'total_pages': total_pages,
        'search_field': search_field,
        'search_value': search_value,
        'search_field_label': FIELD_LABELS.get(search_field, search_field),
        'total': ket_qua_full.count()
    }

    return render(request, 'search_hoso.html', context)

# Thêm hồ sơ
def them_ho_so(request):
    if request.method == 'POST':
        form = HoSoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm hồ sơ thành công.')
            return redirect('tat_ca_ho_so')
    else:
        # ✅ Lấy bản ghi cuối cùng trong bảng (nếu có)
        last_record = HoSo.objects.last()
        if last_record:
            initial_data = {
                'bang_ke_dot_gan': last_record.bang_ke_dot_gan,
                'dot_nhap': last_record.dot_nhap,
                'gb': last_record.gb,
                'bu_dm': last_record.bu_dm,
                'hieu_luc': last_record.hieu_luc,
                'ds_luu': last_record.ds_luu,
                'quan': last_record.quan,
                'lan_nhap': last_record.lan_nhap,
            }
            form = HoSoForm(initial=initial_data)
        else:
            form = HoSoForm()

    return render(request, 'form_ho_so.html', {'form': form, 'action': 'Thêm'})

# Sửa hồ sơ
def sua_ho_so(request):
    so_ho_so = request.GET.get('so_ho_so')
    ho_so = get_object_or_404(HoSo, so_ho_so=so_ho_so)
    if request.method == 'POST':
        form = HoSoForm(request.POST, instance=ho_so)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật hồ sơ thành công.')
            return redirect('tat_ca_ho_so')
    else:
        form = HoSoForm(instance=ho_so)
    return render(request, 'form_ho_so.html', {'form': form, 'action': 'Sửa'})

# Xóa hồ sơ
def xoa_ho_so(request):
    so_ho_so = request.GET.get('so_ho_so')
    ho_so = get_object_or_404(HoSo, so_ho_so=so_ho_so)
    if request.method == 'POST':
        ho_so.delete()
        messages.success(request, 'Đã xóa hồ sơ.')
        return redirect('tat_ca_ho_so')
    return render(request, 'xoa_xac_nhan.html', {'ho_so': ho_so})

def xuat_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "HoSo"

    # Tiêu đề cột
    columns = [
        "Số Hồ Sơ", "Bảng Kê Đợt Gắn", "Đợt Nhập", "DB Cũ", "HD Cũ", "DB Mới", "HD Mới",
        "Đợt", "Giá Biểu", "Bù Định Mức", "Hiệu Lực", "Mã Hợp Đồng", "DS Lưu",
        "Ghi Chú", "Trở Ngại", "Quận", "Lần Nhập"
    ]
    ws.append(columns)

    # Ghi dữ liệu từng dòng
    for ho_so in HoSo.objects.all():
        ws.append([
            ho_so.so_ho_so,
            ho_so.bang_ke_dot_gan,
            ho_so.dot_nhap,
            ho_so.db_cu,
            ho_so.hd_cu,
            ho_so.db_moi,
            ho_so.hd_moi,
            ho_so.dot,
            ho_so.gb,
            ho_so.bu_dm,
            ho_so.hieu_luc,
            ho_so.ma_hd,
            ho_so.ds_luu,
            ho_so.ghi_chu,
            ho_so.tro_ngai,
            ho_so.quan,
            ho_so.lan_nhap,
        ])

    # Xuất response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=HoSo.xlsx'
    wb.save(response)
    return response

def doc_so_quan_568(request):
    lan_nhap_value = request.GET.get('lan_nhap', '').strip()
    data = []

    if lan_nhap_value:
        ho_sos = HoSo.objects.filter(
            lan_nhap=lan_nhap_value,
            quan__in=['Q5', 'Q6', 'Q8']
        ).order_by('hieu_luc', 'quan', 'dot', 'dot_nhap')

        quan_map = {
            'Q5': '5',
            'Q6': '6',
            'Q8': '8',
        }

        for index, hs in enumerate(ho_sos, start=1):
            danh_ba = hs.db_moi if hs.db_moi else hs.db_cu
            hop_dong = hs.hd_moi if hs.hd_moi else hs.hd_cu
            ten_quan = quan_map.get(hs.quan, hs.quan)

            data.append({
                'stt': index,
                'dot_nhap': hs.dot_nhap,
                'danh_ba': danh_ba,
                'hop_dong': hop_dong,
                'dot': hs.dot,
                'hieu_luc': hs.hieu_luc,
                'quan': ten_quan
            })

    tong_so = len(data)

    context = {
        'data': data,
        'lan_nhap_value': lan_nhap_value,
        'tong_so': tong_so
    }
    return render(request, 'doc_so_quan_568.html', context)

# Hàm parse để phục vụ sắp xếp
def parse_hieu_luc(hieu_luc):
    match = re.search(r'(\d{1,2})/(\d{2})', hieu_luc or '')
    if match:
        month = int(match.group(1))
        year = int(match.group(2))
        if year < 100:
            year += 2000
        return (year, month)
    return (0, 0)

# Hàm định dạng hiển thị hiệu lực
def format_hieu_luc(hieu_luc):
    match = re.search(r'(\d{1,2})/(\d{2})', hieu_luc or '')
    if match:
        month = int(match.group(1))
        year = int(match.group(2))
        if year < 100:
            year += 2000
        return f"HIỆU LỰC {month}/{year}"
    return "Không xác định"

def doc_so_binh_tan(request):
    lan_nhap_value = request.GET.get('lan_nhap', '').strip()
    data = []

    if lan_nhap_value:
        ho_sos = HoSo.objects.filter(
            lan_nhap=lan_nhap_value,
            quan='BA'
        ).order_by('hieu_luc', 'dot', 'dot_nhap')

        for index, hs in enumerate(ho_sos, start=1):
            danh_ba = hs.db_moi if hs.db_moi else hs.db_cu
            hop_dong = hs.hd_moi if hs.hd_moi else hs.hd_cu
            hieu_luc_dinh_dang = format_hieu_luc(hs.hieu_luc)

            data.append({
                'stt': index,
                'dot_nhap': hs.dot_nhap,
                'danh_ba': danh_ba,
                'hop_dong': hop_dong,
                'dot': hs.dot,
                'hieu_luc': hieu_luc_dinh_dang,
            })

    tong_so = len(data)

    context = {
        'data': data,
        'lan_nhap_value': lan_nhap_value,
        'tong_so': tong_so,
    }
    return render(request, 'doc_so_binh_tan.html', context)

def to_trinh(request):
    lan_nhap_value = request.GET.get('lan_nhap', '').strip()
    ho_sos = []
    tong_so = 0

    if lan_nhap_value:
        ho_sos = HoSo.objects.filter(
            lan_nhap=lan_nhap_value
        ).filter(
            Q(db_moi__isnull=False) & ~Q(db_moi='') |
            Q(hd_moi__isnull=False) & ~Q(hd_moi='')
        ).select_related().order_by('dot_nhap')
        tong_so = ho_sos.count()

    return render(request, 'to_trinh.html', {
        'ho_sos': enumerate(ho_sos, start=1),
        'lan_nhap_value': lan_nhap_value,
        'tong_so': tong_so
    })

def bao_cao(request):
    # Lấy tất cả hiệu lực có định dạng như "HL 12/24"
    all_hl = HoSo.objects.values_list('hieu_luc', flat=True)

    # Trích xuất phần tháng/năm từ "HL 12/24" -> "12/24"
    valid_hl = []
    for hl in all_hl:
        if hl and '/' in hl:
            parts = hl.strip().split()
            if len(parts) == 2 and '/' in parts[1]:
                valid_hl.append(parts[1])  # Lưu "12/24"

    # Lấy danh sách các năm duy nhất, chuyển "24" -> "2024"
    years = sorted(set(["20" + hl.split('/')[1] for hl in valid_hl]))

    # Năm được chọn từ query string hoặc mặc định là năm cuối
    selected_year = request.GET.get('year', years[-1]) if years else None

    # Danh sách tháng của năm được chọn, dạng "1/24", "2/24", ...
    selected_suffix = selected_year[-2:]  # Lấy "24" từ "2024"
    months = [f"{i}/{selected_suffix}" for i in range(1, 13)]

    # Map tên hiển thị quận -> mã trong CSDL
    district_map = {
        'Q5': 'Q5',
        'Q6': 'Q6',
        'Q8': 'Q8',
        'BTAN': 'BA',
    }

    report_data = []
    totals = defaultdict(int)

    for m in months:
        row = {'month': m}
        total = 0
        for display_name, db_value in district_map.items():
            # So sánh theo phần sau "HL ", tức là chỉ lấy phần tháng/năm
            count = HoSo.objects.filter(hieu_luc__icontains=m, quan=db_value).count()
            row[display_name.lower()] = count
            totals[display_name.lower()] += count
            total += count
        row['total'] = total
        totals['total'] += total
        report_data.append(row)

    context = {
        'years': years,
        'selected_year': selected_year,
        'report_data': report_data,
        'total': {
            'q5': totals['q5'],
            'q6': totals['q6'],
            'q8': totals['q8'],
            'btan': totals['btan'],
            'total': totals['total'],
        }
    }
    return render(request, 'bao_cao.html', context)

def chuyen_kho(request):
    ds_luu_value = request.GET.get('ds_luu', '').strip()
    ho_sos_data = []
    tong_so = 0

    if ds_luu_value:
        ho_sos = HoSo.objects.filter(ds_luu=ds_luu_value).order_by('dot_nhap')

        for index, hs in enumerate(ho_sos, start=1):
            ho_sos_data.append({
                'index': index,
                'bang_ke_dot_gan': hs.bang_ke_dot_gan,
                'dot_nhap': hs.dot_nhap,
                'so_ho_so': hs.so_ho_so,
                'danh_ba': hs.db_moi if hs.db_moi else hs.db_cu,
                'hop_dong': hs.hd_moi if hs.hd_moi else hs.hd_cu,
                'ghi_chu': "Trả ĐM" if hs.bu_dm != '0' else '',
            })

    tong_so = len(ho_sos_data)
    context = {
        'ds_luu_value': ds_luu_value,
        'ho_sos': ho_sos_data,
        'tong_so': tong_so
    }
    return render(request, 'chuyen_kho.html', context)
