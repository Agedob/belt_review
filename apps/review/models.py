from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class BlogManager(models.Manager):
    def simple_validator(self, postData):
        errors = {}
        re_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors["fname"] = "First name shouldn't be empty."
        if len(postData['lname']) < 2:
            errors["lname"] = "Last name shouldn't be empty."
        if not re_email.match(postData['email']):
            errors["email"] = "Email should be standard email characters."
        if len(postData['pw']) < 8:
            errors['pw'] = "Passwords must be longer."
        elif postData['pw'] != postData['cpw']:
            errors['match'] = "Your password didn't match up."
        if User.objects.filter(email = postData['email']):
            errors['email'] = "Invalid email."
        if not errors:
            pass1 = bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=postData['fname'], last_name=postData['lname'], email=postData['email'],password=pass1)
        return errors

    def login_validator(self, POSTS):
        errors = {}
        if len(POSTS['email']) < 1 or len(POSTS['pw']) < 1:
            errors['empty'] = "Fill out Login"
        if not User.objects.filter(email = POSTS['email']):
            errors['email'] = "Wrong email/password"
        else:
            passs = User.objects.get(email=POSTS['email'])
            if not bcrypt.checkpw(POSTS['pw'].encode(), passs.password.encode()):
                errors['passs'] = "Wrong email/password"
        return errors

    def book_validator(self, POSTS, use_id):
        errors = {}
        if len(POSTS['title']) < 3 or len(POSTS['review']) < 3:
            errors['empty'] = "Fill out form"
        if int(POSTS['stars']) == 0:
            errors['rate'] = "Select a rating"
        if len(POSTS['new_auth']) > 3 and Author.objects.filter(author = POSTS['new_auth']):
                errors['auth'] = "Author is in our list"
        if Book.objects.filter(title = POSTS['title']):
            errors["exsists"] = "Title already exsists" 
        if not errors:
            if len(POSTS['new_auth']) > 3:
                aid = Author.objects.create(author = POSTS['new_auth'])
                print aid
                id = Book.objects.create(title = POSTS['title'], authors_id = aid.id)
                print id
                Review.objects.create(rating = POSTS['stars'], comments = POSTS['review'], books_id = id.id, users_id = use_id)
            else:
                aid = Author.objects.get(author = POSTS['author'])
                print aid
                id = Book.objects.create(title = POSTS['title'], authors_id = aid.id)
                print id
                Review.objects.create(rating = POSTS['stars'], comments = POSTS['review'], books_id = id.id, users_id = use_id)
        return errors

    def review_validator(self, POSTS, use_id):
        errors = {}
        if len(POSTS['review']) < 5 or int(POSTS['stars']) == 0:
            errors['empty'] = "Fill out form"
        if not errors:
            Review.objects.create(rating = POSTS['stars'], comments = POSTS['review'], books_id = POSTS['bookid'], users_id = use_id)
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BlogManager() 

class Author(models.Model):
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BlogManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    authors = models.ForeignKey(Author, related_name="book_authors")
    objects = BlogManager()

class Review(models.Model):
    rating = models.IntegerField(default = 0)
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    books = models.ForeignKey(Book, related_name="uploaded_books")
    users = models.ForeignKey(User, related_name="user_reviews")
    objects = BlogManager()



