from django.db import models
from datetime import date, datetime
import re

class RegManager(models.Manager):
    def reg_validator(self, postData):
        errors = {} 
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'first name needs to be longer'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'last name needs to be longer'
        if len(postData['username']) < 5:
            errors['username'] = 'username needs to be longer'
        if len(postData['email']) < 5:
            errors['email'] = 'email needs to be valid'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        og_email = User.objects.filter(email = postData['email'])
        if len(og_email) > 0:
            errors['email'] = 'that email is in use'
        og_username = User.objects.filter(username = postData['username'])
        if len(og_username) > 0:
            errors['username'] = 'that username is in use'
        if len(postData['password']) < 8:
            errors['password'] = 'password is too short'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'password does not match'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=55)
    secondid = models.CharField(max_length=255)  #password
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegManager()

class Book(models.Model):
    title = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    description: models.CharField(max_length=10000)
    ratings = models.IntegerField()
    user = models.ForeignKey(User, related_name = 'reviews')
    book = models.ForeignKey(Book, related_name= 'reviews', blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Author(models.Model):
    name = models.CharField(max_length=55)
    book = models.ManyToManyField(Book, related_name="authors", blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
