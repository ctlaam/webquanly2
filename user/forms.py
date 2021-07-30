from .models import Nguoidung,Baitap
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

class Editnd(ModelForm):
    class Meta:
        model = Nguoidung
        fields = 'ten','gioitinh','ngaysinh','phone'

class u_r(ModelForm):
    class Meta:
        model=User
        fields='username','password','email'

class MyfileUploadForm(forms.Form):
    ten = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    mota = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    giaovienhd = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    filebaocao = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))
    filezip = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

class Editbaitap(ModelForm):
    class Meta:
        model = Baitap
        fields = 'ten','mota','giaovienhd','filebaocao','filezip'