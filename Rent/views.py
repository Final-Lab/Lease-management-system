from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Inventory,RentalRecord,RentApplication
from .forms import RegisterForm, LoginForm, RegistrateUserForm
# from .decorators import user_login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import authenticate, login, logout



def  test(request):
    if request.user.is_authenticated:
        return render(request, 'test.html', {"state": "已登录:"+request.user.username+" id:"+ str(request.user.id)})
    return render(request, 'test.html', {"state": "请登录:"})

@csrf_exempt
def register(request):
    form = RegistrateUserForm()
    if request.method == 'POST':
        form = RegistrateUserForm(request.POST)
        print(request.POST['username'])
        print(request.POST['email'])
        print(request.POST['password1'])
        print(request.POST['password2'])
        if form.is_valid():
            pw1 = request.POST['password1']
            pw2 = request.POST['password2']
            if pw1 != pw2:
                return JsonResponse({'error': "password not same"})
            user = form.save()
            #group = Group.objects.get(name='Users')                    #not sure
            #user.groups.add(group)
            return JsonResponse({'message': "ok"})
        else:
            return JsonResponse({'error': form.errors})
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
                User_name = user.username
                all_rentinfo = RentalRecord.objects.filter(student=User_name)           #not sure
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
