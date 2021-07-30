from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import Editnd,u_r,MyfileUploadForm,Editbaitap
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.views.generic import CreateView
from .models import Nguoidung,Baitap
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorator import unauthenticated_user,allowed_users,admin_only,hocsinh_only


# from .filters import
# Create your views here.

@login_required(login_url="user:dangnhap")
def home(request):
    nd = Nguoidung.objects.get(user__id=request.user.id)
    ur= User.objects.get(id=request.user.id)
    context = {'nd': nd, 'ur':ur}
    return render(request, 'templates/home.html',context)


@unauthenticated_user
def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'Tên người dùng không tồn tại')
            return redirect('/dangnhap')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Sai mật khẩu')
            return redirect('/dangnhap')
        login(request, user)
        return redirect('/')

    return render(request, 'templates/login.html')


@login_required(login_url="user:dangnhap")
def Dangxuat(request):
    logout(request)
    messages.success(request,'Đăng xuất thành công')
    return redirect('/dangnhap')



def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        print(password)

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Tên người dùng để trống hoặc đã tồn tại')
                return redirect('/dangki')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email đã tồn tại')
                return redirect('/dangki')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            group=Group.objects.get(name='hocsinh')
            user_obj.groups.add(group)
            nguoidung_obj = Nguoidung.objects.create(user=user_obj,phone=phone)
            nguoidung_obj.save()

            return redirect('/dangnhap')
        except Exception as e:
            print(e)
    return render(request, 'templates/dangki.html')


class Editprofile(LoginRequiredMixin,View):
    login_url = '/dangnhap/'
    def get(self,request):
        nd=Nguoidung.objects.get(user__id=request.user.id)
        form=Editnd(instance=nd)
        ur=User.objects.get(id=request.user.id)
        form1=u_r(instance=ur)
        context={'nd':form,'ur':form1}
        return render(request,'templates/edit-profile.html',context)
    def post(self,request):
        nd=Nguoidung.objects.get(user__id=request.user.id)
        if request.method=='POST':
            form=Editnd(request.POST,instance=nd)
            if form.is_valid():
                form.save()
                email=request.POST['email']
                ur=User.objects.get(id=request.user.id)
                ur.email=email
                ur.save()
                return redirect('user:home')
            return redirect('user:home')


@admin_only
@login_required(login_url="user:dangnhap")
def dshocsinh(request):
    ds=Nguoidung.objects.all()
    context = {'ds':ds}
    return render(request,'templates/dshocsinh.html',context)



@login_required(login_url="user:dangnhap")
def xoahocsinh(request,pk):
    hocsinh = Nguoidung.objects.get(id=pk)
    if request.method == 'POST':
        hocsinh.delete()
        return redirect('user:danhsachhocsinh')
    context = {'hocsinh':hocsinh}
    return render(request,'templates/xoahocsinh.html',context)

@login_required(login_url="user:dangnhap")
def detailBaitap(request, baitap_id):
    nd = Nguoidung.objects.get(pk=baitap_id)
    return render(request, "templates/baitaphs.html", {"nd": nd})





class Nopbaitap(LoginRequiredMixin,View):
    login_url = '/dangnhap/'
    def get(self,request):
        form=MyfileUploadForm()
        context={'form':form,}
        return render(request,'templates/nopbai.html',context)


    def post(self,request):
        nd=Nguoidung.objects.get(user__id=request.user.id)
        if request.method=='POST':
            form=MyfileUploadForm(request.POST,request.FILES)
            if form.is_valid():
                ten = form.cleaned_data['ten']
                mota = form.cleaned_data['mota']
                gvhd = form.cleaned_data['giaovienhd']
                file_data1 = form.cleaned_data['filebaocao']
                file_data2 = form.cleaned_data['filezip']
                Baitap(ten=ten, mota=mota,giaovienhd=gvhd,filebaocao=file_data1,filezip=file_data2,nguoidung=nd).save()
                return redirect('user:home')
            return redirect('user:home')



# @login_required(login_url="user:dangnhap")
# def Updatebaitap(request,pk):
#     baitap=Baitap.objects.get(id=pk)
#     form = Editbaitap(instance=baitap)
#     nd = Nguoidung.objects.get(user__id=request.user.id)
#     if request.method == 'POST':
#         form=Editbaitap(request.POST,request.FILES,instance=baitap)
#         if form.is_valid():
#             form.save()
#             return redirect('user:home')
#     context={'form':form}
#     return render(request, 'templates/nopbai.html', context)



@login_required(login_url="user:dangnhap")
def Updatebaitap(request,pk):
    baitap=Baitap.objects.get(id=pk)
    form = Editbaitap(instance=baitap)
    if request.method == 'POST':
        form=Editbaitap(request.POST,request.FILES,instance=baitap)
        if form.is_valid():
            form.save()
            return redirect('user:home')
    context={'form':form}
    return render(request, 'templates/nopbai.html', context)


@login_required(login_url="user:dangnhap")
def Xoabaitap(request,pk):
    baitap = Baitap.objects.get(id=pk)
    if request.method == 'POST':
        baitap.delete()
        return redirect('user:home')
    context = {'baitap':baitap}
    return render(request,'templates/xoabaitap.html',context)

