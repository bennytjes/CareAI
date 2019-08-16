from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages, auth
from user.forms import RegistrationForm , UserDetailForm , ProductsRegisterForm
from datetime import date
from .models import *


# Create your views here.


# def login(request):
#     if request.user.is_authenticated():
#         return redirect(request,'/user/profile/')
#     else:
#         #form = AuthenticationForm()
#         args = {'form':form, 'logged_in' : True}
#         #return render(request,'/user/login',args)

# def logout(request):
#     return render(request,'/user/logout')

def register(request): 
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            newUser = {'username':form.cleaned_data.get('username'),
                       'user_id_id':User.objects.get(username = form.cleaned_data.get('username')).pk,}
                    #    'is_supplier':form.cleaned_data.get('is_supplier')}
            newUserRow = UserDetails(**newUser)
            newUserRow.save()
            autoLogin = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password1'],
                                    )
            auth.login(request, autoLogin)
            return redirect('/user/profile/')
        else:
            return render(request, 'reg_form.html', {'form':form})
        
    else:
        form = RegistrationForm()
        args = {'form':form}
        return render(request, 'reg_form.html', args)

def profile(request):
    detail_dict = UserDetails.objects.get(user_id = request.user.id).__dict__
    if None in detail_dict.values():
        return redirect('/user/profile/edit/')
    args={'user':request.user,'detail' : detail_dict,'logged_in' : request.user}
    return render(request,'profile.html',args)


####### Django Auth Profile Edit
# def edit_profile(request):
#     if request.method == 'POST':
#         form = UserChangeForm(request.POST,instance = request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('/user/profile/')
#         else:
#             return redirect('/user/')

#     else:
#         form = UserChangeForm(instance = request.user)
#         args = {'form':form}
        
#         return render(request, 'edit_profile.html',args)

def profile_edit(request):
    if request.method == 'POST':
        form = UserDetailForm(request.POST)
        if form.is_valid():
            p = form.save(commit = False)
            p.user_id_id = request.user.pk
            p.save()
            return redirect('/user/profile/')
    else:
        userdata = UserDetails.objects.get(user_id=request.user.pk).__dict__
        form = UserDetailForm(userdata)
        args = {'form':form,'test':userdata}
        return render(request,'profile_edit.html',args)

def products(request):
    try:
        productdata = Products.objects.filter(user_id = request.user.pk)
    except:
        productdata = None

    args = {'products':productdata}
    return render(request, 'products.html', args)

def products_register(request):
    if request.method == 'POST':
        form = ProductsRegisterForm(request.POST)
        if form.is_valid():
            p = form.save(commit = False)
            p.added_date = date.today()
            p.user_id = request.user
            p.save()
            scoreRow = Scores(product_id_id = p.pk)
            scoreRow.save()
            return redirect('/user/products/')
        else:
            return render(request,'products_register.html',args)
    else:
        form = ProductsRegisterForm()
        args = {'form':form}
        return render(request,'products_register.html',args)

def product_edit(request,product_id):
    productData = Products.objects.get(product_id = product_id)
    request.session['product_id'] = product_id 
    if request.method == 'POST':
        form = ProductsRegisterForm(request.POST)
        if form.is_valid():
            p = form.save(commit = False)
            p.user_id_id = request.user.pk
            p.product_id = product_id
            p.save()
            return render(request, 'product_edit.html',{'form' : form, 'product':productData})
        else:
            return render(request, 'product_edit.html',{'form' : form,'product':productData })
    else:
        form = ProductsRegisterForm(productData.__dict__)
        return render(request, 'product_edit.html',{'form' : form,'product':productData})
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST,user = request.user)
        
        if form.is_valid():
            form.save()
            return redirect('/user/profile/')
    else:
        form = PasswordChangeForm(user = request.user)
        return render(request,'change_password.html',{'form': form})
    