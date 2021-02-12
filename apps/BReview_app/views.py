from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import * # be specific with your classes
import bcrypt

def display_login(request):
    return render (request, 'login.html')

def reg_process(request):
    if 'username' in request.session or 'email' in request.session:
        messages.error(request, 'log out with the current user')
        return redirect ('/')
    errors = User.objects.reg_validator(request.POST)
    if request.method == 'POST':
        if len (errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect ('/')
        elif 'username' in request.session or 'email' in request.session:
            messages.error(request, 'Someone is logged in. Please log out before registering')
            return redirect ('/')
        else:
            pash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                username = request.POST['username'],
                email = request.POST['email'],
                secondid = pash
            )
            messages.success (request, 'Registration completed.')
            current_user = User.objects.filter(username = request.POST['username'])
            request.session['email'] = request.POST['email']
            request.session['first_name'] = request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['username'] = request.POST['username']
            request.session['user_id'] = current_user[0].id
            return redirect ('/user/' + str(request.session['user_id']))
    return HttpResponse ('post request not working')

def user_dashboard(request, user_id):
    page_owner = User.objects.filter(id = user_id)
    context = {
        'page_owner': page_owner
    }
    return render (request, 'user_home.html', context)

def login_process(request):
    if request.method == 'POST':
        user = User.objects.filter(username = request.POST['username'])
        if request.POST['username'] == "" or request.POST['password'] == "":
            messages.error (request, 'please fill out all fields')
            return redirect ('/')
        elif int(len(user)) != 1:
            messages.error(request, 'user does not exist')
            return redirect ('/')
        elif bcrypt.checkpw(request.POST['password'].encode(), user[0].secondid.encode()):
            request.session['user_id'] = user[0].id
            request.session['first_name'] = user[0].first_name
            request.session['last_name'] = user[0].last_name
            request.session['username'] = user[0].username
            request.session['email'] = user[0].email
            return redirect ('/user/' + str(request.session['user_id']))
        else:
            messages.error (request, 'username and password do not match')
            return redirect ('/')
        return redirect ('/user/' + str(request.session['user_id']))
    return HttpResponse ('post request not working')

def logout_process(request):
    if 'username' in request.session or 'email' in request.session or 'user_id' in request.session:
        request.session.flush()
        return redirect('/')
    else:
        request.session.flush()
        messages.error (request, 'nobody is logged in my man')
        return redirect ('/')

def display_books(request):
    return render (request, 'display_book.html')

def book_form(request):
    return render (request, 'create_book.html')

def process_book (request):
    if request.method == 'POST':
        if 'username' in request.session or 'email' in request.session:
            if int(len(Book.objects.filter(title = request.POST['title'])) > 0):
                return HttpResponse ('add a review in the book details page')
            this_user = User.objects.get(id =request.session['user_id'])
            this_book = Book.objects.create(
                title = request.POST['title'],
            )
            book_to_add = this_book
            if len(request.POST['add_author']) > 0:
                this_author = Author.objects.create(
                    name = request.POST['add_author'],
                )
                this_author.book.add(book_to_add)
            else:
                this_author = Author.objects.filter(name = request.POST['author_name'])[0]
                this_author.book.add(book_to_add)
            Review.objects.create(
                description = request.POST['review_description'],
                ratings = request.POST['rating_value'],
                user = this_user,
                book = this_book
            )
        return redirect ('/books/' + str(this_book.id))
    return HttpResponse ('not working')

def display_book(request, book_id):
    return render (request, 'book_detail.html')