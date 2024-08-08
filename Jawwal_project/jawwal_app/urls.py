from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('create',views.create_user),
    path('registration',views.registration),
    path('welcome',views.onboarding),
    path('newbooking/<int:id>',views.reservation),
    path('update/<int:id>', views.update),

    path('edit/<int:id>',views.edit),
    path('comp/<int:user_id>', views.complaints),

    path('login',views.login),

    path('add_booking',views.add_booking),
    path('create_complaint', views.add_comp),
    path('updated/<int:id>', views.update_book),
    path('delete', views.delete),
     path('logout',views.logout),

    
    
    

]