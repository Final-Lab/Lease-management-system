from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import MyUser
from .forms import RegisterForm, LoginForm, RegistrateUserForm
# from .decorators import user_login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import authenticate, login, logout


@csrf_exempt
def register(request):
    form = RegistrateUserForm()
    if request.method == 'POST':
        form = RegistrateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Users')
            user.groups.add(group)
            return JsonResponse({'message': "ok"})
        else:
            return JsonResponse({'error': "you messed up somewhere"})


@csrf_exempt
def my_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            print("We got it")
            return JsonResponse({'message': "ok"})
    else:
        return JsonResponse({"error": "not loged in"})


def get_user(request):
    return MyUser.objects.get(id=request.session['user_id'])


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
    if request.user.is_authenticated:
        if not request.user.groups.filter(name='Provider').exists():
            user = User.objects.get(username=request.user)
            group = Group.objects.get(name='Provider')
            user.groups.add(group)
            return JsonResponse({"user": "succesfull"})
        else:
            return JsonResponse({"error": "User is Provider already"})
    else:
        return JsonResponse({"error": "not logged in"})

