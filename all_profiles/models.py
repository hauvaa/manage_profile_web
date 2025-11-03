from django.db import models

class HoSo(models.Model):
    so_ho_so = models.CharField(primary_key=True, max_length=20)  # Số hồ sơ (Primary Key)
    bang_ke_dot_gan = models.CharField(max_length=20)
    dot_nhap = models.IntegerField()
    db_cu = models.CharField(max_length=20, blank=True, null=True)
    hd_cu = models.CharField(max_length=20, blank=True, null=True)
    db_moi = models.CharField(max_length=20, blank=True, null=True)
    hd_moi = models.CharField(max_length=20, blank=True, null=True)
    dot = models.IntegerField(null=True)
    gb = models.IntegerField()
    bu_dm = models.CharField()
    hieu_luc = models.CharField(max_length=20, null=True)
    ma_hd = models.CharField(max_length=20, blank=True, null=True)
    ds_luu = models.IntegerField(blank=True, null=True)
    ghi_chu = models.TextField(blank=True, null=True)
    tro_ngai = models.TextField(blank=True, null=True)
    quan = models.CharField(max_length=10)
    lan_nhap = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.so_ho_so