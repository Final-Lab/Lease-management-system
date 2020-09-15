from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import EmailValid,Inventory,RentalRecord,RentApplication
from .forms import EmailForm, RegisterForm, LoginForm, RegistrateUserForm
# from .decorators import user_login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import authenticate, login, logout
import random,time
from django.core.mail import send_mail
import hashlib


def  pwd_encrypt(password):                 #encryption function
	md5 = hashlib.md5()
	md5.update(password.encode())
	result = md5.hexdigest()
	return result


def get_random_data():                      #create random num 4 digits
	number = random.randint(1000,9999)
	return number



def test(request):                                                                  #can be removed when test ends
    if request.user.is_authenticated:
        return render(request, 'test.html', {"state": "已登录:"+request.user.username+" id:"+ str(request.user.id)})
    return render(request, 'test.html', {"state": "请登录:"})


def register_page(request):
    return render(request, 'register.html')


@csrf_exempt
def register(request):
    form = RegistrateUserForm()


def register_get_code(request):
    render(request, 'register.html', {"state": ""})
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                number = get_random_data()
                subject = '验证码'                                          # title
                text_content = html_content ="Hello,您的验证码为：%d"%number
                email_valid = EmailValid()
                email_valid.sec_code = number
                email_valid.email = email
                email_valid.save()
                status = send_mail(subject, text_content, '1723225155@qq.com', [email])
                # 参数为主题，内容，寄件人邮箱，以及传递过来的邮箱
            except Exception as err:
                return JsonResponse({"error": str(err)})
            else:                                                                                        #发送验证码成功
                return render(request, 'register.html', {"state": "已获取验证码", "email": email,})        #can be remove later
        else:
            return JsonResponse({"error": "invalid email address"})
    else:
        return JsonResponse({"error": "require POST"})


def register_confirm(request):
    if request.method == 'POST':
        if not User.objects.filter(email=request.POST['email']).exists():
            if EmailValid.objects.filter(email=request.POST['email']).exists():
                form = EmailValid.objects.get(email=request.POST['email'])
                if form.sec_code == request.POST['sec_code']:
                    pw1 = request.POST['password1']
                    pw2 = request.POST['password2']
                    if pw1 != pw2:
                        return JsonResponse({'error': "password not the same"})
                    if User.objects.filter(username=request.POST['username']).exists():
                        return JsonResponse({'error': "Username already exists"})
                    user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                    password = pw1)
                    user.save()
                    #group = Group.objects.get(name='Users')                                    #not sure
                    #user.groups.add(group)
                    return render(request, 'register.html', {"state": "注册成功"})                #can be remove later
                else:
                    return JsonResponse({'error': form.errors})
            else:
                return JsonResponse({'error': "This email_address hasn't get sec_code"})
        else:
            return JsonResponse({'error': "This email_address already registered"})
    else:
        return JsonResponse({"error": "require POST"})


@csrf_exempt
def my_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("We got it")
            return JsonResponse({'message': "ok"})
        else:
            return JsonResponse({"error": "not loged in"})
    else:
        return JsonResponse({"error": "require POST"})


# @user_login_required
@csrf_exempt
def home(request):
    print(request.user)
    if request.user.is_authenticated:
        print("we got it again mate")
        return render(request, 'Rent/home.html')
    else:
        return JsonResponse({"error":"not loged in"})



@csrf_exempt
def mylogout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"user":"logged out"})
    else:
        return JsonResponse({"error":"not loged in"})


@csrf_exempt
def apply_for_provider(request):
    print(request.user)
    if User.objects.filter(username=request.user).exists():
        if not request.user.groups.filter(name='Provider').exists():
            user = User.objects.get(username=request.user)
            #group = Group.objects.get(name='Provider')                     #not sure
            #user.groups.add(group)
            return JsonResponse({"user": "succesfull"})
        else:
            return JsonResponse({"error": "User is Provider already"})
    else:
        return JsonResponse({"error": "not logged in"})


def check_rented_items(request, user_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if User.objects.filter(id=user_id).exists():
                user=User.objects.get(id=user_id)
                all_rentinfo = RentalRecord.objects.filter(student=user.username)           #not sure
                list = []
                if all_rentinfo.exists():
                    for info in all_rentinfo:
                        dict = { "item_id": info.id, 'name': info.item ,'Status': info.status}
                        list.append(dict)
                    response = {"item":list}
                    return JsonResponse(response)
                else:
                    return JsonResponse({"error": "No Data"})
            else:
                return JsonResponse({"error": "User not exists"})
        else:
            return JsonResponse({"error": "not logged in"})
    else:
        return JsonResponse({"error": "require GET"})


def check_all_requests(request, user_id, request_type):
    if request.user.is_authenticated:
        if User.objects.filter(id=user_id).exists():
            all_info = RentApplication.objects.filter(type=request_type)            #not sure
            list = []
            if all_info.exists():
                for item in all_info:
                    dict = {"req_id": item.id, 'status': item.status, 'item': item.student, 'reson': item.reason, 'data': item.date}
                    list.append(dict)
                response = {"request": list}
                return JsonResponse(response)
            else:
                return JsonResponse({"error": "No Data"})
        else:
            return JsonResponse({"error": "User not exists"})
    else:
        return JsonResponse({"error": "not logged in"})


def user_info(request, user_id):
    if request.user.is_authenticated:
        if User.objects.filter(id=user_id).exists():
            user=User.objects.get(id=user_id)
            group="User"
            #all_provider = Group.objects.get(name='Provider').user_set.all()           #not sure
            #if all_provider.filter(id=user.id).exists():
             #   group="Supplier"
            ans_dict = {"username": user.username, 'email': user.email,'data-joined': user.date_joined}
            return JsonResponse(ans_dict)
        else:
            return JsonResponse({"error": "User not exists"})
    else:
        return JsonResponse({"error": "not logged in"})
