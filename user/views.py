from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages, auth
from user.forms import RegistrationForm , UserDetailForm , ProductsRegisterForm
from datetime import date
from .models import UserDetails,Products,Scores


#Registration page view
def register(request): 
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #Save the user in the built-in auth database
            form.save()

            #Create and save the user in the custom UserDetails database
            newUser = {'username':form.cleaned_data.get('username'),
                       'user_id_id':User.objects.get(username = form.cleaned_data.get('username')).pk,}
            newUserRow = UserDetails(**newUser)
            newUserRow.save()

            #Login the user
            autoLogin = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password1'],)
            auth.login(request, autoLogin)
            return redirect('/user/profile/')
        else:
            return render(request, 'reg_form.html', {'form':form})
    
    else: 
        #If request.method == 'GET', show the registration form'
        form = RegistrationForm()
        args = {'form':form}
        return render(request, 'reg_form.html', args)

#Profile page view
def profile(request):
    #Admin doesn't have a profile page, redirect to Home
    if request.user.is_superuser:
        return redirect('/')

    #Get user details to display
    detail_dict = UserDetails.objects.get(user_id = request.user.id).__dict__

    #If there is empty fields, redirect to the edit profile page
    if None in detail_dict.values():
        return redirect('/user/profile/edit/')
    
    #Else just display the profile page
    args={'user':request.user,'detail' : detail_dict,'logged_in' : request.user}
    return render(request,'profile.html',args)


#Edit Profile page
def profile_edit(request):
    
    if request.method == 'POST':
        form = UserDetailForm(request.POST)
        if form.is_valid():
            #Make sure the user has the same id and save it into the custom table
            p = form.save(commit = False)
            p.user_id_id = request.user.pk
            p.save()
            return redirect('/user/profile/')
    else:
        #Prepopulate the fileds with user detail
        userdata = UserDetails.objects.get(user_id=request.user.pk).__dict__
        form = UserDetailForm(userdata)
        args = {'form':form,'test':userdata}
        return render(request,'profile_edit.html',args)

#Products page view
def products(request):
    #Try to get a list of products from the user. Return None if there is no product yet.
    try:
        productdata = Products.objects.filter(user_id = request.user.pk)
    except:
        productdata = None

    args = {'products':productdata}
    return render(request, 'products.html', args)

#Product Registration page view
def products_register(request):
    if request.method == 'POST':
        form = ProductsRegisterForm(request.POST)
        if form.is_valid():
            #Overwrite the add_date and user_id before saving it 
            p = form.save(commit = False)
            p.added_date = date.today()
            p.user_id = request.user
            p.save()
            #Create an empty row for storing completeness score
            scoreRow = Scores(product_id_id = p.pk)
            scoreRow.save()
            return redirect('/user/products/')
        else:
            args = {'form':form}
            return render(request,'products_register.html',args)
    else:
        form = ProductsRegisterForm()
        args = {'form':form}
        return render(request,'products_register.html',args)

#Edit products page view
def product_edit(request,product_id):
    #Load the current product_id from the session, and get the product detials
    request.session['product_id'] = product_id 
    product = get_object_or_404(Products,pk = product_id).__dict__
    oneToTen = range(1,11)
    args = {'product_id':product_id,
            'productInfo':product,
            'oneToTen':oneToTen}
    productData = Products.objects.get(product_id = product_id)
    request.session['product_id'] = product_id 

    if request.method == 'POST':
        form = ProductsRegisterForm(request.POST)
        #Overwrite the user_id and product_id to make sure it's not changed
        if form.is_valid():
            p = form.save(commit = False)
            p.user_id_id = request.user.pk
            p.product_id = product_id
            p.save()
            args['form'] = form
            args['product'] = productData
            return render(request, 'product_edit.html',args)
        else:
            args['form'] = form
            args['product'] = productData
            return render(request, 'product_edit.html',args)
    else:
        #Prepopulate the fields
        form = ProductsRegisterForm(productData.__dict__)
        args['form'] = form
        args['product'] = productData
        return render(request, 'product_edit.html',args)
    
#Change Password page view
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            #Save the password and log in the user
            form.save()
            autoLogin = auth.authenticate(username=request.user,
                                     password=form.cleaned_data['new_password1'],)
            auth.login(request, autoLogin)
            return redirect('/user/profile/')

    else:
        form = PasswordChangeForm(user = request.user)
        return render(request,'change_password.html',{'form': form})
    