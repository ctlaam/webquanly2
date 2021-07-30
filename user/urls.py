from django.urls import path
from .views import *
app_name= 'user'
urlpatterns = [
    path('', home,name='home'),
    path('dangnhap/',login_attempt,name='dangnhap'),
    path('dangxuat/',Dangxuat,name='dangxuat'),
    path('dangki/',register_attempt,name='dangki'),
    path('chinhsuathongtin/',Editprofile.as_view(),name='csthongtin'),
    path('dshocsinh/',dshocsinh,name='danhsachhocsinh'),
    path('xoahocsinh/<str:pk>/', xoahocsinh, name='xoahocsinh'),
    path('baitap/<int:baitap_id>', detailBaitap, name='baitap'),
    path('nopbaitap/',Nopbaitap.as_view(),name='nopbaitap'),
    path('updatebaitap/<str:pk>', Updatebaitap, name='updatebaitap'),
    path('xoabaitap/<str:pk>/', Xoabaitap, name='xoabaitap'),
]