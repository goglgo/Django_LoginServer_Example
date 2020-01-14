from django.shortcuts import render, redirect, Http404, HttpResponse
from django.http import JsonResponse
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm as LoginForm

# Create your views here.

# return JsonResponse({'foo':'bar'})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            res = {
                'status':'success',
                'id' : username,
                'user_type':user.profile.user_type
            }
            return JsonResponse(res)
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def return_json_response(status, username=None):
    res = {
        'status':status,
    }
    if(username):
        res['id'] = username
    return JsonResponse(res)

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            res = {
                'status':'success',
                'id':username,
                'user_type':user.profile.user_type
            }
            return JsonResponse(res)
            # return redirect('index')
        else:
            # return HttpResponse('로그인 실패. 다시 시도 해보세요.')
            return return_json_response('로그인 실패. 다시 시도해주세요.')
    else:
        form = LoginForm()
        return render(request, 'accounts/signin.html', {'form': form})