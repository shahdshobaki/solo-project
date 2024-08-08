from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
# python ma.py collectstatic
# GET requests
def index(request):
    return render(request, 'login.html')

def onboarding(request):
    id = request.session['user_id']
    context ={
        'user': User.objects.get(id=id),
        'books': get_books(),
    }
    return render(request, 'onboarding.html',context)

def reservation(request,id):
    context ={
        'user': User.objects.get(id=id)
    }
    return render(request, 'reservation.html',context)

# def update(request):
#     id = request.session['user_id']
#     context = {
#         'user': User.objects.get(id=id),  
#         'books': get_booking(),  
#     }
#     return render(request, 'update.html', context)
    
def edit(request,id ):
    context ={
        'book': get_booking(id)
    }
    return render(request, 'edit.html',context)

# def complaints(request, user_id):
#     user_id = request.session['user_id']  # Ensure the session ID is used
    
#     # Fetch the user object
#     user = User.objects.get(id=user_id)
    
#     # Fetch books or complaints related to this user
#     books = get_books(user_id)  # Pass user_id to get_books if it's designed that way
    
#     context = {
#         'user': user,  # Pass the user object to the template
#         'books': books,  # Pass the related books/complaints
#     }
#     return render(request, 'comp.html', context)

def complaints(request, user_id):
    user_id = request.session['user_id']
   
    context = {
        'user': User.objects.get(id=user_id),  # Fetch user based on session user_id
        'books': get_books(),  # Assuming this needs the 'id' passed as an argument
    }
    return render(request, 'comp.html', context)





#handel request post to registration, and pass data to the method to it there are an error shown a msg and redirect to registration page, else create the data and go to the success
def registration(request):
    if request.method == 'POST':
        errors = User.objects.basic_register(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():   
                messages.error(request, value)    
            return redirect('/')
        else:
            user = create_user(request.POST)
            request.session['user_id'] = user.id
            messages.success(request, "Successfully Registered")
            return redirect('/welcome')
    return redirect('/')

#handel request post to login by user email, and pass data to the method if there are an error display a msg and redirect to main page, else create the data and go to the success page
def login(request):
  if request.method == 'POST':
        errors = User.objects.basic_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        user = check_email(request.POST) 
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect ('/welcome')
            

## to get the users and books بجيب داتا    
def bookings(request):
  if 'user_id' not in request.session:
      return redirect('/')
  else:
      context = {
          'user': get_user(request.session),
          'books': get_books(),
          # 'upload_by':upload_by()
      }
  return render(request, 'onboarding.html',context)

#add booking 

def add_booking(request):
#   if 'user_id' not in request.session:
#       return redirect('/')
#   if request.method== 'POST':
#       errors = Appointment.objects.basic_book_appointment(request.POST)
#       if len(errors) > 0:
#           for key, value in errors.items():   
#               messages.error(request, value)    
#           return redirect('/add_booking')
#       else:
        create_booking(request)
        return redirect('/welcome')
      
### add complaints     
def add_comp(request):
    create_complaints(request)
    request.session['user_id'] 
    messages.success(request, "Your complaint was added successfully. We will get back to you within 72 working hours.")
    return render(request, 'comp.html')


#update the booking

def update(request, book_id):
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id),  
        'book': get_booking(book_id)  
    }
    return render(request, 'update.html',context)

def update_book(request):
   
    update_booking(request)
    return redirect('/welcome')
   
        
#delete booking

def delete(request):
    if request.method =='POST':
     delete_booking(request.POST)
    # request.session['user_id'] 
    # messages.success(request, "Your booking deleted successfully")
    return redirect('/welcome')

# clear the session of user to logout
def logout(request):
    if request.method=='POST':
        request.session.clear()
        return redirect('/')

