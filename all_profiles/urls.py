from django.urls import path
from . import views

urlpatterns = [
    path('', views.trang_chu, name='trang_chu'),
    path('tat-ca-ho-so/', views.tat_ca_ho_so, name='tat_ca_ho_so'),
    path('them/', views.them_ho_so, name='them_ho_so'),
    path('sua/', views.sua_ho_so, name='sua_ho_so'),
    path('xoa/', views.xoa_ho_so, name='xoa_ho_so'),
    path('xuat-excel/', views.xuat_excel, name='xuat_excel'),
    path('search/',views.search_hoso, name='search_hoso'),
    path('doc-so-quan-568/', views.doc_so_quan_568, name='doc_so_quan_568'),
    path('doc-so-binh-tan/', views.doc_so_binh_tan, name='doc_so_binh_tan'),
    path('to-trinh/', views.to_trinh, name='to_trinh'),
    path('bao-cao/', views.bao_cao, name='bao_cao'),
    path('chuyen-kho/', views.chuyen_kho, name='chuyen_kho'),
]