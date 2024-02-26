from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.views import View
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib import messages
from restaurantadminapp.models import *

# Create your views here.                                                                                                                                                                                                                                                                                                            

class AdminDashboard(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser is True:
                total_user=CustomUser.objects.all().filter(is_superuser=False).count()
                active=CustomUser.objects.all().filter(is_superuser=False,is_active=True).count()
                in_active=CustomUser.objects.all().filter(is_superuser=False,is_active=False).count()
                total_restaurant=RestaurentDetails.objects.all().count()
                active_restaurant=RestaurentDetails.objects.all().filter(is_active=True).count()
                inactive_restaurant=RestaurentDetails.objects.all().filter(is_active=False).count()
                
                return render(request,'admin/dashboard.html',{'total_user':total_user,'active':active,'in_active':in_active,'total_restaurant':total_restaurant,'active_restaurant':active_restaurant,'inactive_restaurant':inactive_restaurant})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login')
        

def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email_id = request.POST.get('email_id')
            passwords = request.POST.get('password')
            user = authenticate(
                request=request, email_id=email_id, password=passwords)
            print(user,'user')
            if user is not None:
                if CustomUser.objects.filter(email_id=email_id, is_superuser=True):
                    dj_login(request, user)
                    return redirect('admin-dashboard')
                else:
                    messages.warning(request, 'You Are Not Admin User')
            else:
                messages.warning(request, 'Invalid Email or Password')

        return render(request, 'admin/login.html')
    else:
        return redirect('admin-dashboard')


def Admin_logout(request):
    logout(request)
    messages.success(request, 'Admin Logged Out Successfully..!!')
    return redirect('admin-login')




class Change_password(View):
    
    def get(self, request):
        if  request.user.is_authenticated:
            if request.user.is_superuser is True:
                return render(request, 'admin/password_reset.html')
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login') 
    def post(self, request):
        id=request.user.id
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if old_password and new_password and confirm_password:
            if new_password == confirm_password:
                new_password = confirm_password
                user = CustomUser.objects.get(id=id)
                check=user.check_password(old_password)
            
                if check==True:
                    user.set_password(new_password)
                    user.save()
                    
                    messages.success(request, 'New password  Successfully..!!')
                    return redirect("admin-dashboard")
                else:

                    messages.error(request, 'Incorrect Old Password..!!')

            else:
                messages.warning(request, 'please check your newpassword and confirm password..!!')

        else:
            messages.info(request, 'Old Password and New password and Confirm password is required!!!')
        return redirect('change-password')

############################################################
class Forget_password(View):
    def get(self, request):
        return render(request, 'admin/forget.html')

    def post(self, request):
        email_id = request.POST.get('email_id')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if email_id and new_password and confirm_password:
            if CustomUser.objects.filter(email_id=email_id,is_superuser=True).exists():
                if new_password == confirm_password:
                    new_password = confirm_password
                    user = CustomUser.objects.get(email_id=email_id,is_superuser=True   )
                    user.set_password(new_password)
                    user.save()
                    messages.success(request,'Password Changed..!!!')
                    return redirect('admin-login')
                else:
                    messages.warning(request, 'please check your newpassword and confirm password..!!')
            else:
                messages.error(request, 'email id is not exist')
        else:
            messages.info(
                request, 'Email_id and New_password and Confirm_password is required')
        return redirect('forgot-password')
    


#########################Show users ###############

class Add_Users(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser is True:
                return render(request,'admin/users/add_users.html')
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login')
    def post(self,request):
        choose_profilepic=request.FILES.get('choose_profilepic')
        email_id=request.POST.get('email_id')
        full_name=request.POST.get('full_name')
        phone_number=request.POST.get('phone_number')
        CustomUser.objects.create(choose_profilepic=choose_profilepic,email_id=email_id,full_name=full_name,phone_number=phone_number,password=1234)
        
        return redirect('show-users')

class Show_Users(View):
    def get(self,request):
        if  request.user.is_authenticated:
            if request.user.is_superuser is True:
                users = CustomUser.objects.filter(is_superuser=False).all()
                return render(request,'admin/users/show_users.html',{'Users':users})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login')



class Edit_Users(View):
    def get(self, request, id):
        if  request.user.is_authenticated:
            if request.user.is_superuser is True:
                data = CustomUser.objects.get(pk=id)
                return render(request, 'admin/users/edit_users.html', {'datas': data})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login')
    def post(self, request, id):
        data=CustomUser()
        choose_profilepic=request.FILES.get('choose_profilepic')
        email_id=request.POST.get('email_id')
        full_name=request.POST.get('full_name')
        phone_number=request.POST.get('phone_number')
        if choose_profilepic is not None:
            data =CustomUser.objects.get(pk=id)
            data=CustomUser(id=id,choose_profilepic=choose_profilepic,email_id=email_id,full_name=full_name,phone_number=phone_number,password=request.user.password).save()
        else:
            data =CustomUser.objects.get(pk=id)
            data=CustomUser(id=id,choose_profilepic=data.choose_profilepic,email_id=email_id,full_name=full_name,phone_number=phone_number,password=request.user.password).save()
        return redirect('show-users')


def Delete_Users(request ,id):
        if request.method=='POST':
            if request.user.is_superuser is True:
                pi=CustomUser.objects.get(pk=id)
                print(pi,'ppi')
                pi.delete()
        return redirect('show-users')


def Show_Profile(request,id):
    if  request.user.is_authenticated:
        if request.user.is_superuser is True:
            data = CustomUser.objects.get(pk=id)
            return render(request, 'admin/users/profile.html', {'datas': data})
        else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
    else:
        return redirect('admin-login')


class Active_inActive(View):

    def post(self, request):
        user_id = request.POST['id']

        user = CustomUser.objects.get(id=user_id)
        if user.is_active is False:
            user.is_active = True
            user.save()
            return redirect('show-users')

        elif user.is_active is True:
            user.is_active = False
            user.save()
            return redirect('show-users')

   
        else:
            return HttpResponse("User Not Valid")
        
class Edit_Admin(View):
    def get(self, request, id):
        if  request.user.is_authenticated:
            if request.user.is_superuser is True:
                data = CustomUser.objects.get(pk=id)
                return render(request, 'admin/users/edit_admin.html', {'datas': data})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login ')
    def post(self, request, id):
        choose_profilepic=request.FILES.get('choose_profilepic')
        full_name=request.POST.get('full_name')
        phone_number=request.POST.get('phone_number')
        if choose_profilepic is not None:
            data =CustomUser.objects.get(pk=id)
            data=CustomUser(id=id,choose_profilepic=choose_profilepic,full_name=full_name,email_id=request.user.email_id,phone_number=phone_number,password=request.user.password,   is_admin=True,is_superuser=True,is_active=True).save()
        else:
            data =CustomUser.objects.get(pk=id)
            data=CustomUser(id=id,choose_profilepic=data.choose_profilepic,email_id=request.user.email_id,full_name=full_name,phone_number=phone_number,password=request.user.password,is_admin=True,is_superuser=True,is_active=True).save()
        return redirect('admin-dashboard')




class Add_Rastaurant(View):
    def get(self,request):
        if request.user.is_superuser is True:
            data=CustomUser.objects.all().filter(is_superuser=False)
            return render(request,'admin/manage_restaurent/add_restaurent.html',{'data':data})
        else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
    def post(self,request):
        id=request.POST.get('id')
        
        user_id=CustomUser.objects.get(id=id)
        print(user_id)
        restaurant_name=request.POST.get('restaurant_name')
        restaurant_id=request.POST.get('restaurant_id')
        restaurant_address=request.POST.get('restaurant_address')
        RestaurentDetails.objects.create(user_id=user_id,restaurant_name=restaurant_name,restaurant_id=restaurant_id,restaurant_address=restaurant_address)
        return redirect('show-restaurant')
    
class Show_Restaurant(View):
    def get(self,request):
        if request.user.is_superuser is True:
            data=RestaurentDetails.objects.all()
            return render(request,'admin/manage_restaurent/show_restaurant.html',{'data':data})
        else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
    

class Restaurant_detail(View):
    def get(self,request,id):
        if request.user.is_superuser is True:
            data=RestaurentDetails.objects.get(id=id)
            print(data.qr_code,'name')
            return render(request,'admin/manage_restaurent/show_details.html',{'data':data})
        else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
    

def Delete_Restaurant(request ,id):
    if request.user.is_superuser is True:
        if request.method=='POST':
            pi=RestaurentDetails.objects.get(pk=id)
            print(pi,'ppi')
            pi.delete()
        return redirect('show-restaurant')
    else:
                messages.error(request,'You are not admin')
                return redirect('user-login')


class User_Payment(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser is True:
                data=RestaurentDetails.objects.all().order_by('restaurant_name')
                return render(request,'admin/payment.html',{'data':data})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login')


class Add_SubscriptionsDetails(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser is True:
                return render(request,'admin/subscription_details/add_subscription_details.html')
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login')
    
    def post(self,request):
        heading=request.POST.get('heading')
        subscription_price=request.POST.get('subscription_price')
        subscription_duration=request.POST.get('subscription_duration')
        SubscriptionDetails.objects.create(heading=heading,subscription_duration=subscription_duration,subscription_price=subscription_price)
        return redirect('show-subscription')

class Show_SubscriptionsDetails(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser is True:
                data=SubscriptionDetails.objects.all()
                return render(request,'admin/subscription_details/show_subscription_details.html',{'data':data})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login')
        

class Edit_SubscriptionsDetails(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            if request.user.is_superuser is True:
                data=SubscriptionDetails.objects.get(id=id)
                return render(request,'admin/subscription_details/update_subscription_details.html',{'data':data})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login')
    def post(self,request,id):

        heading=request.POST.get('heading')
        subscription_price=request.POST.get('subscription_price')
        subscription_duration=request.POST.get('subscription_duration')
        SubscriptionDetails(id=id,heading=heading,subscription_duration=subscription_duration,subscription_price=subscription_price).save()
        return redirect('show-subscription')

def delete_subscriptionsdetails(request,id):
    if request.user.is_superuser is True:
        if request.method=='POST':
            data=SubscriptionDetails.objects.get(id=id)
            data.delete()
        return redirect('show-subscription')
    else:
            messages.error(request,'You are not admin')
            return redirect('user-login')
            
        

class Restaurant_Active_inActive(View):

    def post(self, request):
        user_id = request.POST['id']

        user = RestaurentDetails.objects.get(id=user_id)
        if user.is_active is False:
            user.is_active = True
            user.save()
            return redirect('show-restaurant')

        elif user.is_active is True:
            user.is_active = False
            user.save()
            return redirect('show-restaurant')

   
        else:
            return HttpResponse("User Not Valid")
        




def handler404(request, exception):
    return render(request, 'admin/page404.html', status=404)




class Add_Notifiactions(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser is True:
                data=CustomUser.objects.all().filter(is_superuser=False)
                return render(request,'admin/add_notifications.html',{'datas':data})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
            
        else:
                return redirect('admin-login')
    def post(self,request):
        heading=request.POST.get('heading')
        description=request.POST.get('description')
        receiver = request.POST.getlist("receiver")
        print(receiver)
        
        try:
            if receiver ==['']:
                data=CustomUser.objects.all().filter(is_superuser=False)
                for data in data:
                    Notification.objects.create(heading=heading,description=description,receiver=data,sender=request.user.full_name)
                return redirect('show-notification')

            else:   
                for receiver in receiver:
                    
                    receiveruser=CustomUser.objects.get(id=int(receiver))
                    Notification.objects.create(heading=heading,description=description,receiver=receiveruser,sender=request.user.full_name )
                return redirect('show-notification')
        except ValueError:
            messages.error(request,'Select either allusers or only users')
            return redirect('sent-notification')
class Notifiactions_show(View):
    def get(self,request):
        if request.user.is_superuser is True:    
            users = Notification.objects.all().order_by('-created_by')

            return render(request,'admin/show_notification.html',{'Users':users})
        else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        

def delete_notifications(request,id):
        if request.user.is_superuser is True:
            if request.method=='POST':    
                users = Notification.objects.get(id=id)
                users.delete()

            return redirect('show-notification')
            
        else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        
def delete_all_notifications(request):
        if request.user.is_superuser is True:   
            if request.method=='POST': 
                users = Notification.objects.all()
                users.delete()

            return redirect('show-notification')
        else:
                messages.error(request,'You are not admin')
                return redirect('user-login')