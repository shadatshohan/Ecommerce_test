from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout,authenticate,login
from Product.models import Category,Product,Images
from django.contrib import messages
from EcomApp.models import Setting 
from UserApp.models import UserProfile
from UserApp.forms import SignUpForm

# Create your views here.
def user_logout(request):
	logout(request)
	return redirect('home')

def user_login(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.warning(request,'Your username or password is invalid')
	category=Category.objects.all()
	setting=Setting.objects.get(id=1)
	context={'category':category,'setting':setting}
	return render(request,'UserApp/user_login.html',context)

def user_register(request):
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			password=form.cleaned_data.get('password1')
			user=authenticate(username=username,password=password)
			login(request,user)
			return redirect('home')
		else:
			messages.warning(request,'Your new and old password do not match')
	else:
		form=SignUpForm()
	category=Category.objects.all()
	setting=Setting.objects.get(id=1)
	context={'category':category,'setting':setting,'form':form}
	return render(request,'UserApp/user_register.html',context)