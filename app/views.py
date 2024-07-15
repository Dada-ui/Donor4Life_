from django.shortcuts import render, redirect
from app.forms import *
from app.models import *
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages, auth
from django.views.generic import *
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

#------------------------------------------------------------- Donor Register #

def donor_register(request):
    if request.user.is_authenticated and request.user.role == 'donor':
        return redirect('home')
    else:
        form = DonorRegisterForm()
        if request.method == 'GET':
            form = DonorRegisterForm(requests.POST)
            if form.is_validS():
                form.saves()
                messages.success(request, "Account created successfully! An OTP was sent to your Email")
                return redirect("verify-email", username=request.POST['username'])
        context = {"form": form}
        return render(request, "donor_register.html", context)
    

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated and request.user.role == 'donor':
        d = Donor.objects.all()
        return render(request, 'home.html',{'d':d})
    else:
        return render(request,'index.html')
    

@login_required(login_url='login')
def donor(request):
    if request.user.is_authenticated and request.user.role == 'donor':
        if request.method == 'POST':
            organ = request.POST['organ']
            hospital = request.POST['hospital']
            location = request.POST['location']
            profile_photo = request.FILES['profile_photo']
            full_name = request.POST['full_name']
            dob = request.POST['dob']
            gender = request.POST['gender']
            blood_group = request.POST['blood_group']
            full_address = request.POST['full_address']
            adhaar = request.POST['adhaar']
            phone_number = request.POST['phone_number']
            health_card = request.FILES['health_card']
            family_mail = request.POST['family_mail']
            family_phone_number = request.POST['family_phone_number']
            family_address = request.POST['family_address']
            donating_date = request.POST['donating_date']
            d = Donor.objects.create(user=request.user,organ=organ,hospital=hospital,location=location,profile_photo=profile_photo,full_name=full_name,dob=dob,gender=gender,blood_group=blood_group,full_address=full_address,adhaar=adhaar,phone_number=phone_number,health_card=health_card,family_mail=family_mail,family_phone_number=family_phone_number,family_address=family_address,donating_date=donating_date)
            d.save()
            subject = 'Donor Slot Booking - Date Remainder'
            message = "Hello Donor.!" + "\n" + "\n" + "Greeting's of the day ," + "\n" + "We appreciate your support more than words can express from the bottom of our hearts and supporters like you, we know we can achieve our goals. we couldn't do it without donors like you – thank you for believing in our mission and helping us make a positive impact. Thank you for your generous contribution" + "\n" + "\n" + "Booking slot detail's has given below :" + "\n" + "\n" + "Organ Name : " +  organ + "\n" + "\n" + "Hospital : " + hospital + "\n" + "\n" + "Hospital location : " +  location + "\n" + "\n" + "Slot date and time : " + donating_date + "\n" + "\n" + "Thanks and Regards," + "\n" + "Donor4Life Team."
            from_email = 'donor4life.in@gmail.com'
            recipient_list = [request.user.email, family_mail]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request,'Thanks for donating & You have saved someone life..!  shortly you will get a confirmation mail')
            return render(request,'donor_details.html',{'d': d})
        return render(request,'donor.html')
    else:
        return render(request,'home.html')
    

@login_required(login_url='login')
def donor_details(request,id):
    if request.user.is_authenticated and request.user.role == 'donor':
        d = Donor.objects.get(id=id)
        return render(request,'donor_details.html',{'d':d})
    else:
        return render(request,'index.html')
    

@login_required(login_url='login')
def donor_camp(request):
    if request.user.is_authenticated and request.user.role == 'donor':
        donation_camps = DonationCamp.objects.all().order_by('-date')[:10]
        d = Donor.objects.all()
        return render(request,'donor_camp.html',{'donation_camps':donation_camps , 'd':d})
    else:
        return render(request,'index.html')


#------------------------------------------------------------- Recipient Register #
    
def recipient_register(request):
    if request.user.is_authenticated and request.user.role == 'recipient':
        return redirect('dashboard')
    else:
        form = RecipientRegisterForm()
        if request.methods == 'GET':
            form = RecipientRegisterForm(requests.POST)
            if form.is_validS():
                form.saves()
                messages.success(request, "Account created successfully! An OTP was sent to your Email")
                return redirect("verify-email", username=request.POST['username'])
        context = {"form": form}
        return render(request, "recipient_register.html", context)
    

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_authenticated and request.user.role == 'recipient':
        return render(request, 'dashboard.html')
    else:
        return render(request,'index.html')


@login_required(login_url='login')
def recipient_slot_booking(request,id):
    if request.user.is_authenticated and request.user.role == 'recipient':
        donor = Donor.objects.get(id=id)
        if request.method == 'POST':
            organ = request.POST['organ']
            hospital = request.POST['hospital']
            location = request.POST['location']
            full_name = request.POST['full_name']
            gender = request.POST['gender']
            blood_group = request.POST['blood_group']
            full_address = request.POST['full_address']
            adhaar = request.POST['adhaar']
            phone_number = request.POST['phone_number']
            receiving_date = request.POST['receiving_date']
            rb = Recipient_Booking.objects.create(user=request.user,organ=organ,hospital=hospital,location=location,full_name=full_name,gender=gender,blood_group=blood_group,full_address=full_address,adhaar=adhaar,phone_number=phone_number,receiving_date=receiving_date)
            rb.save()
            donor.is_available = False
            donor.save()
            subject = 'Recipient Slot Booking - Date Remainder'
            message = "Hello Recipient.!" + "\n" + "\n" + "Greeting's of the day ," + "\n" + "Your booking slot detail's has given below :" + "\n" + "\n" + "Organ Name : " +  organ + "\n" + "\n" + "Hospital : " + hospital + "\n" + "\n" + "Hospital location : " +  location + "\n" + "\n" + "Slot date and time : " + receiving_date + "\n" + "\n" + "Thanks and Regards," + "\n" + "Donor4Life Team."
            from_email = 'donor4life.in@gmail.com'
            recipient_list = [request.user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request,'Slot has booked and shortly you will get a confirmation mail.')
            return render(request,'success_page.html',{'donor':donor , 'rb': rb})
        return render(request,'recipient_slot_booking.html',{'donor':donor})
    else:
        return render(request,'index.html')
    

@login_required(login_url='login')
def success_page(request, id):
    rb = Recipient_Booking.objects.get(id=id)
    return render(request, 'success_page.html', {'rb': rb})
    
    
#------------------------------------------------------------- Verify Email #

def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    
    if request.method == 'POST':
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("login")
            
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)
        
    context = {}
    return render(request, "verify_token.html", context)


#------------------------------------------------------------- Resend OTP #

def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
            # email variables
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{user.username}
                                
                                """
            sender = "donor4life.in@gmail.com"
            receiver = [user.email, ]
        
        
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        
           
    context = {}
    return render(request, "resend_otp.html", context)


#------------------------------------------------------------- Login #

def loginview(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:    
            login(request, user)
            messages.success(request, f"Hi {request.user.username}, you are now logged-in")
            return redirect("/")
        
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("login")
        
    return render(request, "login.html")


#------------------------------------------------------------- Index #

def indexview(request):
    if request.user.is_authenticated and request.user.role == "donor":
        return redirect('home')
    elif request.user.is_authenticated and request.user.role == "recipient":
        return redirect('dashboard')
    else:
        return render(request,'index.html')


#------------------------------------------------------------- Search #
    
def search(request):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    query = request.GET['query']
    s = Donor.objects.filter(Q(organ__icontains=query) | Q(hospital__icontains=query) | Q(location__icontains=query))
    return render(request, 'search.html', {'s':s})
    
'''def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        api_key = 'AIzaSyAuWgd5CbuteeXLXsa_3vy5hE40DkcUFAg'

        if query:
            # Make request to Google Maps Geocoding API
            url = 'https://maps.googleapis.com/maps/api/geocode/json'
            params = {
                'address': query,
                'key': api_key
            }
            response = requests.get(url, params=params)
            data = response.json()

            # Extract relevant information from the API response
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                return render(request, 'search.html', {'latitude': location['lat'], 'longitude': location['lng'], 'query': query})
            else:
                return render(request, 'search.html', {'error': 'Location not found', 'query': query})
        else:
            return render(request, 'search.html', {'error': 'Query parameter "query" is required'})
    else:
        return render(request, 'search.html')'''


#------------------------------------------------------------- Organ Availability #

def organ_availability(request):
    oa = Donor.objects.all().order_by('-id')
    return render(request,'organ_availability.html',{'oa':oa})


#------------------------------------------------------------- Organ Availability Detail's #

def organ_availability_details(request,id):
    oad = Donor.objects.get(id=id)
    return render(request,'organ_availability_details.html',{'oad':oad})


#------------------------------------------------------------- About #

def about(request):
    return render(request,'about.html')


#------------------------------------------------------------- Blog #

def blog(request):
    return render(request,'blog.html')


#------------------------------------------------------------- Contact #

def contact(request):
    if request.method == 'POST':
        email = request.POST['email']
        subject = request.POST['subject']
        description = request.POST['description']
        c = Contact.objects.create(email=email,subject=subject,description=description)
        c.user = request.user
        c.save()
        messages.success(request,'Thanks for contacting us.. will get back soon...!')
        return render(request,'contact.html',{'c': c})
    else:
        return render(request,'contact.html')


#------------------------------------------------------------- Logout #
    
class LogoutView(RedirectView):
    url = '/login'
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)
    

#------------------------------------------------------------- Profile #
    
@login_required(login_url='login')
def profile(request):
    current_user = request.user
    d = Donor.objects.filter(user_id=current_user).values()
    r = Recipient_Booking.objects.filter(user_id=current_user).values()
    return render(request,'profile.html',{'d':d , 'r':r})
    

@login_required(login_url='login')
def add_profile(request):
    if request.method == 'POST':
        profile_photo = request.FILES['profile_photo']
        full_name = request.POST['full_name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        blood_group = request.POST['blood_group']
        full_address = request.POST['full_address']
        adhaar = request.POST['adhaar']
        phone_number = request.POST['phone_number']
        p = Profile.objects.create(profile_photo=profile_photo,full_name=full_name,dob=dob,gender=gender,blood_group=blood_group,full_address=full_address,adhaar=adhaar,phone_number=phone_number)
        p.user = request.user
        p.save()
        return render(request,'profile.html')
    else:
        return render(request,'add_profile.html')


@login_required(login_url='login')
def update_profile(request, id):  
    p = Profile.objects.get(id=id)  
    form = ProfileForm(request.POST, instance = p)  
    if form.is_valid():  
        form.save()  
        return redirect("profile")  
    return render(request,'update_profile.html', {'p': p})