from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re, datetime, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def register(self, data):
		errors= []
		if len(data['f_name'])<2:
			errors.append("First Name must be at least 2 characters")
		if not data['f_name'].isalpha():
			errors.append("First Name must letters")
		if len(data['alias'])<2:
			errors.append("Alias must be at least 2 characters")
		if len(data['password'])<8:
			errors.append("Password must be at least 8 characters")
		if not data['password']==data['con_pw']:
			errors.append("Password and confirm password doesn't match")
		if len(data['email'])<1:
			errors.append("Email cannot be blank!")
		elif not EMAIL_REGEX.match(data['email']):
			errors.append("email format is wrong!")
		else:
			pass
		try:
			User.objects.get(email = data['email'])
			errors.append("email already exixst!")
		except:
			pass
		if data['dob'] == '':
			errors.append("Birthday is required.")
		elif datetime.datetime.strptime(data['dob'], '%Y-%m-%d') >= datetime.datetime.now():
			errors.append("Birthday may not be in the future!!")
		if len(errors) == 0:
			user = User.objects.create(first_name = data['f_name'], alias_name = data['alias'],email = data['email'], password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()))
			return {'user':user,"error":None}
		else:
			return{'user':None,"error":errors}
	def login(self, data):
		errors= []
		try:
			dbemail=User.objects.get(email = data['email'])
			print dbemail
			print dbemail.password
			print bcrypt.hashpw(data['password'].encode('utf-8'), dbemail.password.encode('utf-8'))
			print User.objects.get(email = data['email'])
			print "*"*50
			if bcrypt.hashpw(data['password'].encode('utf-8'), dbemail.password.encode('utf-8')) == dbemail.password.encode('utf-8'):
				print "*"*50
				return {'user':dbemail,"error":None}
			else:
				errors.append("email password doesn't match!")
				return{'user':None,"error":errors}
		except:
			errors.append("email doesn't exist!")
			return{'user':None,"error":errors}

class QuoteManager(models.Manager):
	def checkquote(self,data):
		errors= []
		if len(data['content']) < 10:
			errors.append("Please add quote content more then 10 characters!")
		if len(data['quoteby']) <3:
			errors.append("Please add quote by more then 3 characters!")
		if len(errors) == 0:
			print "success*************"
			quote1 = Quote(content =data['content'], quoteby = data['quoteby'],creater = data['creater'])
			quote1.save()
			print Quote.objects.all()
			return{'quote':quote1,"error":None}
		else:
			return{'quote':None,"error":errors}
class User(models.Model):
	first_name = models.CharField(max_length=45)
	alias_name = models.CharField(max_length=45)
	email = models.CharField(max_length=145)
	password = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Quote(models.Model):
	content = models.TextField(max_length=500)
	quoteby = models.CharField(max_length=45)
	creater = models.ForeignKey(User, related_name='quote_created')
	favbyuser = models.ManyToManyField(User, related_name="favquote")
	objects = QuoteManager()
