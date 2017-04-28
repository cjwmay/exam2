from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Count
from models import User,Quote
import re, datetime, bcrypt
# Create your views here.
def index(request):
	return render(request, "examapp/index.html")
def logout(request):
	request.session.flush()
	return redirect('/main')
def checkregister(request):
	if request.method == "POST":
		data  = {
			"f_name" : request.POST['f_name'],
			"alias" : request.POST['alias'],
			"email" : request.POST['email'],
			"password": request.POST["con_pw"],
			"con_pw": request.POST["con_pw"],
			'dob': request.POST['birthdate'],
		}
		print data['email']
		result = User.objects.register(data)
		if result['error'] == None:
			request.session['user'] = result['user'].alias_name
			request.session['userid'] = result['user'].id
			return redirect('/quotes')
		else:
			for error in result['error']:
				messages.add_message(request,messages.ERROR,error)
			print result['error']
			return redirect('/main')
	else:
		messages.add_message(request,messages.ERROR,'Please Login or register')
		return redirect('/main')
def checklogin(request):
	if request.method == "POST":
		data  = {
			"email" : request.POST['email'],
			"password": request.POST['password'],
		}
		result = User.objects.login(data)
		if result['error'] == None:
			request.session['user'] = result['user'].alias_name
			request.session['userid'] = result['user'].id
			return redirect('/quotes')
		else:
			for error in result['error']:
				messages.add_message(request,messages.ERROR,error)
			print result['error']
			print User.objects.all().values()
			return redirect('/main')
	return redirect('/main')
def success(request):
	try:
		request.session['user']
		print Quote.objects.all()
		print request.session['userid']
		user = User.objects.get(id = request.session['userid'])
		unfavquotes = Quote.objects.exclude(favbyuser = user)
		print unfavquotes
		favquotes = Quote.objects.filter(favbyuser = user)
		print favquotes
		context = {
			"unfavquotes" : unfavquotes,
			"favquotes" : favquotes,
		}
		return render(request,"examapp/success.html",context)
	except:
		messages.add_message(request,messages.ERROR,"Please Log in!!!!")
		return redirect('/main')
def addquote(request):
	if request.method == "POST":
		content = request.POST['quotemessage']
		quoteby = request.POST['quoteby']
		user = User.objects.get(id = request.session['userid'])
		data = {
			"content":content,
			"quoteby":quoteby,
			"creater":user,
			"favbyuser":user,
		}
		result = Quote.objects.checkquote(data)
		if result['error'] == None:
			return redirect('/quotes')
		else:
			for error in result['error']:
				messages.add_message(request,messages.ERROR,error)
			print result['error']
			return redirect('/quotes')
	return redirect('/quotes')
def addfav(request):
	if request.method == "POST":
		quoteid = request.POST['quoteid']
		quote1 = Quote.objects.get(id = quoteid)
		user1 = User.objects.get(id = request.session['userid'])
		user1.favquote.add(quote1)
		return redirect('/quotes')
def remove(request):
	if request.method == "POST":
		quoteid = request.POST['quoteid']
		quote1 = Quote.objects.get(id = quoteid)
		user1 = User.objects.get(id = request.session['userid'])
		user1.favquote.remove(quote1)
		return redirect('/quotes')
def userbyid(request,id):
	try:
		request.session['user']
		User.objects.annotate(Count('quote_created'))
		user = User.objects.get(id = id)
		users = User.objects.filter(id = id)
		count = user.quote_created.count()
		print count
		quotes = Quote.objects.filter(creater = user)
		context = {
			"users":users,
			"quotes":quotes,
		}
		return render(request, "examapp/user1.html",context)
	except:
		messages.add_message(request,messages.ERROR,"Please Log in!!!!")
		return redirect('/main')
# Create your views here.
