from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import SupplyAplication, RentApplication, Inventory, EmailValid
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrateUserForm
import random
from django.core.mail import send_mail
import hashlib


def pwd_encrypt(password):  # encryption function
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def get_random_data():  # create random num 4 digits
    number = random.randint(1000, 9999)
    return number

@csrf_exempt
def test(request):  # can be removed when test ends
    if request.user.is_authenticated:
        return render(request, 'Rent/test.html',
                      {"state": "已登录:" + request.user.username + " id:" + str(request.user.id)})
    return render(request, 'Rent/test.html', {"state": "请登录:"})

@csrf_exempt
def register_page(request):
    return render(request, 'Rent/register.html')


@csrf_exempt
def register(request):
    form = RegistrateUserForm()

@csrf_exempt
def register_get_code(request):
    #render(request, 'Rent/register.html', {"state": ""})
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        if email:
            try:
                number = get_random_data()
                subject = '验证码'  # title
                text_content = "Hello,您的验证码为：%d" % number
                email_valid = EmailValid()
                email_valid.sec_code = number
                email_valid.email = email
                email_valid.save()
                status = send_mail(subject, text_content, 'bighomeworkcodesender@gmail.com', [email])
                # 参数为主题，内容，寄件人邮箱，以及传递过来的邮箱
            except Exception as err:
                return JsonResponse({"error": str(err)})
            else:  # 发送验证码成功
                return JsonResponse({"msg": "Code send"})
        else:
            return JsonResponse({"error": "invalid email address"})
    else:
        return JsonResponse({"error": "require POST"})

@csrf_exempt
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
                                                    password=pw1)
                    user.save()
                    group = Group.objects.get(name='User')                                    #not sure
                    user.groups.add(group)
                    return JsonResponse({'user': 'registered ' + user.username})
                else:
                    return JsonResponse({'error': form.errors})
            else:
                return JsonResponse({'error': "This email address does not have sec_code"})
        else:
            return JsonResponse({'error': "This email is already registered"})
    else:
        return JsonResponse({"error": "require POST"})


@csrf_exempt
def my_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # print("We got it")
            l = request.user.groups.values_list('name', flat=True)  # QuerySet Object
            l_as_list = list(l)
            ans_dict = {
                'message': "ok",
                'user_id': user.pk,
                "username": user.username,
                'email': user.email,
                'data-joined': user.date_joined,
                'groups': l_as_list
            }
            return JsonResponse(ans_dict)
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
        return JsonResponse({"error": "not loged in"})


@csrf_exempt
def mylogout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"user": "logged out"})
    else:
        return JsonResponse({"error": "not loged in"})


@csrf_exempt
def apply_for_supplier(request):
    if request.user.is_authenticated:
        user_id = request.POST.get('user_id')
        if not request.user.groups.filter(name='Supplier').exists():
            user = User.objects.get(pk=user_id)
            if not SupplyAplication.objects.filter(student=user, status='Pending'):
                apply = SupplyAplication(student=user, status='Pending')
                apply.save()
                return JsonResponse({"apply": "successful"})
            else:
                return JsonResponse({"error": "you've applied already"})
        else:
            return JsonResponse({"error": "User is Supplier already"})
    else:
        return JsonResponse({"error": "not logged in"})


@csrf_exempt
def apply_for_item(request, item_id):
    if request.method == 'POST':

        if request.user.is_authenticated:
            if Inventory.objects.filter(pk=item_id).exists():

                item = Inventory.objects.get(pk=item_id)
                user = User.objects.get(username=request.user)
                if item.status == 'Available':
                    m = RentApplication(item=item,
                                        student=user,
                                        status='Pending',
                                        reason='Cool',
                                        type='Rent')
                    m.save()

                    return JsonResponse({"msg": "ok"})
                else:
                    return JsonResponse({"error": "item is not available"})
            else:
                return JsonResponse({"error": "item does not exist"})
        else:
            return JsonResponse({"error": "not logged in"})


@csrf_exempt
def check_rented_items(request, user_id):
    if request.method == 'GET':
        print(user_id)
        if request.user.is_authenticated:
            if User.objects.filter(id=user_id).exists():
                user = User.objects.get(id=user_id)
                # User_name = user.username
                all_rentinfo = RentApplication.objects.filter(student=user, type='Rent')  # not sure
                list = []
                if all_rentinfo.exists():
                    for info in all_rentinfo:
                        dict = {"item_id": info.item.id,
                                'name': info.item.name,
                                'Status': info.item.status,
                                }
                        list.append(dict)
                    print(list)
                    response = {"item": list}
                    return JsonResponse(response)
                else:
                    return JsonResponse({"error": "No Data"})
            else:
                return JsonResponse({"error": "User not exists"})
        else:
            return JsonResponse({"error": "not logged in"})
    else:
        return JsonResponse({"error": "require GET"})


@csrf_exempt
def check_all_requests(request, user_id, request_type):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if User.objects.filter(id=user_id).exists():
                user = User.objects.get(id=user_id)
                all_info = RentApplication.objects.filter(student=user, type=request_type)  # not sure
                list = []
                if all_info.exists():
                    for item in all_info:
                        dict = {"req_id": item.id,
                                'status': item.status,
                                'item': item.item.name,
                                'reason': item.reason,
                                'data': item.date}
                        list.append(dict)
                    response = {"request": list}
                    return JsonResponse(response)
                else:
                    return JsonResponse({"error": "No Data"})
            else:
                return JsonResponse({"error": "User not exists"})
        else:
            return JsonResponse({"error": "not logged in"})


@csrf_exempt
def user_info(request, user_id):
    if request.user.is_authenticated:
        if User.objects.filter(id=user_id).exists():
            user = User.objects.get(id=user_id)
            l = request.user.groups.values_list('name', flat=True)  # QuerySet Object
            l_as_list = list(l)
            ans_dict = {
                "username": user.username,
                'email': user.email,
                'data-joined': user.date_joined,
                'groups': l_as_list
            }

            return JsonResponse(ans_dict)
        else:
            return JsonResponse({"error": "User not exists"})
    else:
        return JsonResponse({"error": "not logged in"})


@csrf_exempt
def apply_add_item(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.groups.filter(name="Supplier").exists():
                name = request.POST.get('item_name')
                user = User.objects.get(username=request.user)
                if Inventory.objects.filter(name=name).exists():
                    return JsonResponse({"error": "you have the item already"})

                new_item = Inventory(name=name, status="Waiting approval", supplier=user)
                new_item.save()
                m = RentApplication(item=new_item, student=user, status='Pending', reason='Cool', type='Add')
                m.save()
                return JsonResponse({"msg": "ok"})
            else:
                return JsonResponse({"error": "user is not a Supplier"})
        else:
            return JsonResponse({"error": "not logged in"})
    else:
        return JsonResponse({"error": "Expected POST"})


@csrf_exempt
def edit_item(request, item_id, user_id):
    if request.method == 'POST':

        if request.user.is_authenticated:
            if request.user.groups.filter(name="Supplier").exists():
                new_name = request.POST.get('item_name')
                print(new_name)
                if Inventory.objects.filter(pk=item_id).exists():
                    item = Inventory.objects.get(pk=item_id)
                    print(item)
                    # user = User.objects.get(pk=user_id)
                    item.name = new_name
                    item.save()

                    return JsonResponse({"msg": "ok"})
                else:
                    return JsonResponse({"error": "no such item"})
            else:
                return JsonResponse({"error": "user is not a Supplier"})

        else:
            return JsonResponse({"error": "not logged in"})
    else:
        return JsonResponse({"error": "Expected POST"})


@csrf_exempt
def check_item_application(request, user_id, req_id, action):
    if request.method == 'POST':
        print(action)
        print(req_id)
        if request.user.is_authenticated:
            if request.user.groups.filter(name="Supplier").exists():
                if RentApplication.objects.filter(pk=req_id).exists():
                    req = RentApplication.objects.get(pk=req_id)
                    if action == 'accept':
                        req.status = 'Accepted'
                        item = req.item
                        item.status = 'Taken'
                        item.save()
                        req.item = item
                        req.save()

                        return JsonResponse({"msg": "accepted"})

                    if action == 'decline':
                        req.status = 'Declined'
                        req.save()

                        return JsonResponse({"msg": "declined"})
                else:
                    return JsonResponse({"error": "no such item"})
            else:
                return JsonResponse({"error": "user is not a Supplier"})
        else:
            return JsonResponse({"error": "not logged in"})
    else:
        return JsonResponse({"error": "Expected POST"})


@csrf_exempt
def return_rented_item(request, item_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if Inventory.objects.filter(pk=item_id).exists():
                item = Inventory.objects.get(pk=item_id)
                item.status = 'Available'
                item.save()

                return JsonResponse({"msg": "ok"})
            else:
                return JsonResponse({"error": "no such item"})

        else:
            return JsonResponse({"error": "not logged in"})
    else:
        return JsonResponse({"error": "Expected POST"})


@csrf_exempt
def view_all_items(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if User.objects.filter(username=request.user).exists():
                user = User.objects.get(username=request.user)
                # User_name = user.username
                all_rentinfo = Inventory.objects.filter()  # not sure
                list = []
                if all_rentinfo.exists():
                    for info in all_rentinfo:
                        dict = {"item_id": info.id,
                                'name': info.name,
                                'Status': info.status,
                                }
                        list.append(dict)
                    print(list)
                    response = {"list": list}
                    return JsonResponse(response)
                else:
                    return JsonResponse({"error": "No Data"})
            else:
                return JsonResponse({"error": "User not exists"})
        else:
            return JsonResponse({"error": "not logged in"})
    else:
        return JsonResponse({"error": "require GET"})
