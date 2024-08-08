from django.db import models
import re
import bcrypt
from django.core.exceptions import ObjectDoesNotExist

class UserManager(models.Manager): # validation for login and registration
    def basic_register(self, postData): # function for registration 
        errors = {}
        if len(postData['first_name']) < 2:# validated first name
            errors["first_name"] = "First Name should be at least 2 characters"## as list ""if satament
            # errors["first_name"].append=('')
        if len(postData['last_name']) < 2:# validated last name
            errors["last_name"] = "Last Name should be at least 2 characters"
        # validated dob to required in database and age grater than 13"
        #validated format of mail and unique email used
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):             
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email=postData['email']).exists():
            errors['email_used'] = "Email already in use!"
        # validated pass to be greater than 8 char and match with confirm pass 
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['repassword']:
            errors["confirm_pw"] = "Passwords are not match "
        return errors
    
    def basic_login(self, postData):# function for login 
            errors = {}
            try:
                user = User.objects.get(email=postData['email'])
            except ObjectDoesNotExist:
                errors['email'] = "Email not found."
                return errors
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid password or Username."
            return errors
    
class AppointmentManager(models.Manager):
    def basic_book_appointment(self, postData): # function for book
        errors = {}
        if len(postData['jawwal-number']) == 10:
            errors["jawwal-number"] = "رقم الجوال يحب ان يكون 10 خانات"
        return errors



    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Changed max_length to 255
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #appointms

   


class Appointment(models.Model):
    reason = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    showroom_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    time = models.TimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='appointments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()


class Complaint(models.Model):
    description = models.CharField(max_length=255)
    visitor = models.ForeignKey(User, related_name="complaints", on_delete=models.CASCADE)

# create user 

def create_user(POST):
    password = POST['password']
    return User.objects.create(
        first_name=POST['first_name'],
        last_name =POST['last_name'],
        email=POST['email'],
    
        password= bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
        )

# get user to session
def get_user(session):
    return User.objects.get(id=session['user_id'])

#check user mail
def check_email(POST):
    return User.objects.filter(email=POST['email'])

#to get all Appointment by their IDs 

def get_booking(id):
    return Appointment.objects.get(id=id)



def get_books():
    return Appointment.objects.all()

#update the booking
def update_booking(POST,book_id):
   
    booking =Appointment.objects.get(id=book_id)
    booking.reason=POST['reason']
    booking.city=POST['city']
    booking.showroom_name=POST['showroom_name']
    booking.start_date=POST['start_date']
    booking.mobile=POST['jawwal-number']
    booking.time=POST['time']
    booking.save()

#delete the booking


def delete_booking(POST):
    book_remove=Appointment(POST['id_appointment'])
    book_remove.delete()


#create booking
def create_booking(request):
        id = request.session['user_id']
        user = User.objects.get(id = id)
        print(user)
        POST= request.POST
        #Appointment.objects.create( reason= "test test",  city="121323", showroom_name = "WB" , start_date = "2024-07-07" , mobile= "0599001770" , time="23:00"  , user = user)
        Appointment.objects.create(
        reason=POST['reason'],
        city=POST['city'],
        showroom_name=POST['showroom_name'],
        start_date=POST['start_date'],
        mobile=POST['jawwal-number'],
        time=POST['time'],
        user = user)

#create complaints

def create_complaints(request):
    id = request.session['user_id']
    user = User.objects.get(id=id)
    print(user)
    POST = request.POST
    Complaint.objects.create(
        description=POST['description'],
        visitor=user
        
    )




