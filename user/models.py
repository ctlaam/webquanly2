from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Nguoidung(models.Model):
    ten = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex_choice = (('Nam', 'Nam'), ('Nữ', 'Nữ'))
    gioitinh = models.CharField(max_length=10, choices=sex_choice, default='', null=True)
    ngaysinh = models.DateField(null=True)
    phone = models.CharField(max_length=15, null=True,)
    def __str__(self):
        return self.user.username

class Baitap(models.Model):
    nguoidung = models.ForeignKey(Nguoidung,on_delete=models.CASCADE,null=True)
    ten = models.CharField(max_length=50, null=True)
    mota = models.CharField(max_length=1000, null=True)
    giaovienhd =models.CharField(max_length=50, null=True)
    filebaocao = models.FileField(upload_to='')
    filezip = models.FileField(upload_to='')

    def __str__(self):
        return self.ten
