from app import views
from django.urls import path


urlpatterns = [
    path('',views.indexview,name='index'),
    path('search',views.search,name='search'),
    path('organ_availability',views.organ_availability,name='organ_availability'),
    path('organ_availability_details/<int:id>',views.organ_availability_details,name='organ_availability_details'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('blog',views.blog,name='blog'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('login', views.loginview, name='login'),
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),


    #------------------ Donor #
    path('donor_register',views.donor_register,name='donor_register'),
    path('home',views.home,name='home'),
    path('donor',views.donor,name='donor'),
    path('donor_details/<int:id>',views.donor_details,name='donor_details'),
    path('donor_camp',views.donor_camp,name='donor_camp'),


    #------------------ Recipient #
    path('recipient_register',views.recipient_register,name='recipient_register'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('recipient_slot_booking/<int:id>',views.recipient_slot_booking,name='recipient_slot_booking'),
    path('success_page',views.success_page,name='success_page'),

    
    #------------------ Profile #
    path('profile',views.profile,name='profile'),
    path('add_profile',views.add_profile,name='add_profile'),
    path('update_profile/<int:id>',views.update_profile,name='update_profile'),
]