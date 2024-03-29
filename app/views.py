from django.shortcuts import render

# Create your views here.
from app.forms import *

from app.models import *

from django.http import HttpResponse,HttpResponseRedirect

from django.urls import reverse

from django.core.mail import send_mail



from django.contrib.auth import authenticate,login,logout


from django.contrib.auth.decorators import login_required




def registration(request):
    UFO=userform()

    d={'user':UFO}
    if request.method=='POST':
        ufd=userform(request.POST)
       
        if ufd.is_valid():
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()
            
            return HttpResponse('Registration is successfully')
        else:
            return HttpResponse('user already register...')
    return render(request,'registration.html',d)



def home_page(request):
    if request.session.get('username'):
        un=request.session.get('username')
        d={'username':un}
        return render(request,'home_page.html',d)
    return render(request,'home_page.html')







def user_login(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        AUO=authenticate(username=un,password=pw)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=un
            return HttpResponseRedirect(reverse('home_page'))
        else:
            return HttpResponse('Provide Vaild User And Password...')
        
    return render (request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))


@login_required
def changepassword(request):
    if request.method=='POST':
        pw=request.POST['pw']
        un=request.session.get('username')
        Uo=User.objects.get(username=un)
        Uo.set_password(pw)
        Uo.save()
        return HttpResponse('password change successfully....')
    return render(request,'changepassword.html')