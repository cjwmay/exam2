from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, data):
        errors= []
        if len(data['f_name'])<2:
            errors.append("First Name must be at least 2 characters")
        if not data['f_name'].isalpha():
            errors.append("First Name must letters")
        if len(data['l_name'])<2:
            errors.append("Last Name must be at least 2 characters")
        if not data['l_name'].isalpha():
            errors.append("Last Name must letters")
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
        if len(errors) == 0:
            user = User.objects.create(first_name = data['f_name'], last_name = data['l_name'],email = data['email'], password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()))
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


class User(models.Model):
      first_name = models.CharField(max_length=45)
      last_name = models.CharField(max_length=45)
      email = models.CharField(max_length=145)
      password = models.CharField(max_length=100)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = UserManager()
