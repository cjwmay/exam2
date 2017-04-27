from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import User
import bcrypt
# Create your views here.
def index(request):
	return render(request, "examapp/index.html")
def checkregister(request):
	if request.method == "POST":
		data  = {
			"f_name" : request.POST['f_name'],
			"l_name" : request.POST['l_name'],
			"email" : request.POST['email'],
			"password": request.POST["con_pw"],
			"con_pw": request.POST["con_pw"],
		}
		print data['email']
		result = User.objects.register(data)
		if result['error'] == None:
			request.session['user'] = result['user'].first_name + result['user'].last_name
			return redirect('/success')
		else:
			for error in result['error']:
				messages.add_message(request,messages.ERROR,error)
			print result['error']
			return redirect('/')
	else:
		messages.add_message(request,messages.ERROR,'Please Login or register')
		return redirect('/')
def checklogin(request):
	if request.method == "POST":
		data  = {
			"email" : request.POST['email'],
			"password": request.POST['password'],
		}
		result = User.objects.login(data)
		if result['error'] == None:
			request.session['user'] = result['user'].first_name + result['user'].last_name
			return redirect('/success')
		else:
			for error in result['error']:
				messages.add_message(request,messages.ERROR,error)
			print result['error']
			print User.objects.all().values()
			return redirect('/')
	return redirect('/')
def success(request):
	return render(request,"examapp/success.html")


# Create your views here.
