from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from .models import *

def index(request):
    return render(request,'review/index.html', {'everyone':User.objects.all()})

def regi(request):
    if request.method != 'POST':
        messages.error(request, "Create User")
        return redirect('/')
    else:
        errors = User.objects.simple_validator(request.POST)
        if len(errors):
            for key,values in errors.iteritems():
                messages.success(request, values)
            return redirect('/')
        else:
            id = User.objects.get(email=request.POST['email']).id
            name = User.objects.get(email=request.POST['email']).first_name
            request.session['id'] = id
            request.session['name'] = name
            return redirect('/books')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key,values in errors.iteritems():
            messages.success(request, values)
        return redirect('/')
    else:
        id = User.objects.get(email=request.POST['email']).id
        name = User.objects.get(email=request.POST['email']).first_name
        request.session['id'] = id
        request.session['name'] = name
        return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect('/')

def books(request):
    if not 'id' in request.session:
        messages.error(request, "Login")
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['id'])
        content = {'reviewz':Review.objects.all().order_by("-created_at")[:3], "user": user}
        # x = User.objects.get(id = request.session['id'])
        # content = {"reviews":x.user_reviews.all(),'user':x}
        return render(request, 'review/books.html', content)

def add(request):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    else:
        content = {'reviewz': Author.objects.all()}
        # for throuh / if / filter 
        return render(request, 'review/add_book.html', content)
# rave ex

def adding_book(request):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    else:
        errors = Book.objects.book_validator(request.POST,request.session['id'])
        if len(errors):
            for key,values in errors.iteritems():
                messages.success(request, values)
            return redirect('/add_book')
        else:
            return redirect('/books')
    return redirect('/books')

def reviewz(request,num):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    else:
        book = Book.objects.get(id = num)
        author = Author.objects.get(id = book.authors_id)
        content = {'book': book, 'author':author,'reviewz':book.uploaded_books.all()}
        return render(request,'review/comment.html', content)
# important.
def add_review(request):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    else:
        errors = Review.objects.review_validator(request.POST,request.session['id'])
        if len(errors):
            for key,values in errors.iteritems():
                messages.success(request, values)
            return redirect('/book/' + request.POST['bookid'])
        else:
            return redirect('/books')

def myspace(request,num):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    else:
        x = User.objects.get(id = num)
        count = x.user_reviews.all().count()
        content = {"reviews":x.user_reviews.all(),'user':x, 'count': count}
        return render(request, 'review/user.html',content)
