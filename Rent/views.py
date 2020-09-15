from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import authenticate, login, logout



def  test(request):
    if request.user.is_authenticated:
        return render(request, 'Rent/test.html', {"state": "已登录:"+request.user.username+" id:"+ str(request.user.id)})
    return render(request, 'Rent/test.html', {"state": "请登录:"})



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
            group = Group.objects.get(name='Users')                    #not sure
            user.groups.add(group)
            return JsonResponse({'message': "ok"})
        else:
            return JsonResponse({'error': form.errors})
    else:
        return JsonResponse({"error": "require POST"})



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



def home(request):
    print(request.user)
    if request.user.is_authenticated:
        print("we got it again mate")
        return render(request, 'Rent/home.html')
    else:
        return JsonResponse({"error":"not loged in"})




def mylogout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"user":"logged out"})
    else:
        return JsonResponse({"error":"not loged in"})



def apply_for_supplier(request):

    if request.user.is_authenticated:
        user_id = request.POST.get('user_id')
        if not request.user.groups.filter(name='Supplier').exists():
            user = User.objects.get(pk= user_id)
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



def apply_for_item(request, item_id):
    if request.method == 'POST':

        if request.user.is_authenticated:

            item = Inventory.objects.get(pk=item_id)
            user = User.objects.get(username=request.user)
            if item.status == 'Available':
                m = RentApplication(item = item,
                                    student=user,
                                    status='Pending',
                                    reason='Cool',
                                    type='Rent')
                m.save()

                return JsonResponse({"msg": "ok"})
            else:
                return JsonResponse({"error": "item is not available"})

        else:
            return JsonResponse({"error": "not logged in"})



def check_rented_items(request, user_id):
    if request.method == 'GET':
        print(user_id)
        if request.user.is_authenticated:
            if User.objects.filter(id= user_id).exists():
                user= User.objects.get(id= user_id)
                User_name = user.username
                all_rentinfo = RentApplication.objects.filter(student=user, type='Rent')           #not sure
                list = []
                if all_rentinfo.exists():
                    for info in all_rentinfo:
                        dict = { "item_id": info.item.id,
                                 'name': info.item.name ,
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




def check_all_requests(request, user_id, request_type):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if User.objects.filter(id=user_id).exists():
                user = User.objects.get(id=user_id)
                all_info = RentApplication.objects.filter(student=user, type=request_type)            #not sure
                list = []
                if all_info.exists():
                    for item in all_info:
                        dict = {"req_id": item.id,
                                'status': item.status,
                                'item': item.item.name,
                                'reson': item.reason,
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


def user_info(request, user_id):
    if request.user.is_authenticated:
        if User.objects.filter(id=user_id).exists():
            user=User.objects.get(id=user_id)
            l = request.user.groups.values_list('name', flat=True)  # QuerySet Object
            l_as_list = list(l)
            ans_dict = {
                "username": user.username,
                'email': user.email,
                'data-joined': user.date_joined,
                'group': l_as_list[0]
                    }

            return JsonResponse(ans_dict)
        else:
            return JsonResponse({"error": "User not exists"})
    else:
        return JsonResponse({"error": "not logged in"})



def apply_add_item(request):
    if request.method == 'POST':

        if request.user.is_authenticated:
            name = request.POST.get('item_name')

            user = User.objects.get(username=request.user)
            if Inventory.objects.filter(name=name).exists():
                return JsonResponse({"error": "you have the item already"})

            new_item = Inventory(name = name, status="Waiting approval", supplier=user)
            new_item.save()
            m = RentApplication(item = new_item,student=user, status='Pending', reason='Cool', type='Add')
            m.save()
            return JsonResponse({"user": "it happened"})

        else:
            return JsonResponse({"error": "not logged in"})



def edit_item(request, item_id, user_id):
    if request.method == 'POST':

        if request.user.is_authenticated:
            new_name = request.POST.get('item_name')
            print(new_name)
            if Inventory.objects.filter(pk = item_id).exists():
                item = Inventory.objects.get(pk = item_id)
                print(item)
                user = User.objects.get(pk=user_id)
                item.name = new_name
                item.save()

                return JsonResponse({"msg": "ok"})
            else:
                return JsonResponse({"error": "no such item"})

        else:
            return JsonResponse({"error": "not logged in"})



def check_item_application(request, user_id,req_id,action):
    if request.method == 'POST':
        print(action)
        print(req_id)
        if request.user.is_authenticated:
            if RentApplication.objects.filter(pk = req_id).exists():
                req = RentApplication.objects.get(pk = req_id)
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
            return JsonResponse({"error": "not logged in"})



def return_rented_item(request, item_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if Inventory.objects.filter(pk = item_id).exists():
                item = Inventory.objects.get(pk = item_id)
                item.status = 'Available'
                item.save()

                return JsonResponse({"msg": "ok"})
            else:
                return JsonResponse({"error": "no such item"})

        else:
            return JsonResponse({"error": "not logged in"})
