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
                subs=CustomUser.objects.filter(payment_status='Successfull',is_superuser=False).count()
                print(subs)
                return render(request,'admin/dashboard.html',{'total_user':total_user,'active':active,'in_active':in_active,'subs':subs})
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

        new_password = confirm_password
        user = CustomUser.objects.get(id=id)
        check=user.check_password(old_password)
    
        if check==True:
            user.set_password(new_password)
            user.save()
            
            messages.success(request, 'New password  Successfully..!!')
            return redirect("admin-dashboard")
        else:

            messages.error(request, '**Incorrect Old Password..!!')

        
        return redirect('change-password')



class ForgotPassword(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request,'admin/forget.html')
        else:
            return redirect('admin-dashboard')
    def post(self,request):
        email_id=request.POST.get('email_id')
        new_password=request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if CustomUser.objects.filter(email_id=email_id,is_superuser=True).exists():
            user=CustomUser.objects.get(email_id=email_id)
            if new_password==confirm_password:
                user.set_password(new_password)
                user.save()
            
                messages.success(request, 'New password  Successfully..!!')
                return redirect("admin-login")
            else:
                messages.error(request,"New password and Confirm password should be same!")
                return redirect('forgot-password')
        else:
            messages.warning(request,"Email id doesnot exist.")
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
        restaurant_name=request.POST.get('restaurant_name')
        restaurant_logo=request.FILES.get('restaurant_logo')
        email_id=request.POST.get('email_id')
        phone_number=request.POST.get('phone_number')
        restaurant_address=request.POST.get('restaurant_address')
        password=request.POST.get('password')
        userdata=CustomUser.objects.create_user(email_id=email_id,phone_number=phone_number,password=password,restaurant_name=restaurant_name,restaurant_address=restaurant_address,restaurant_logo=restaurant_logo,user_id=userdata)
        print(userdata)
        
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
                data=CustomUser.objects.get(id=id)
                return render(request, 'admin/users/edit_users.html', {'datas': data})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login')
    def post(self, request, id):
        rname=request.POST.get('restaurant_name')
        rlogo=request.FILES.get('restaurant_logo')
        address=request.POST.get('restaurant_address')
        phone_number=request.POST.get('phone_number')
        data=CustomUser.objects.get(id=id)
       
        print(rname,rlogo,address)
        if rlogo is not None:
            CustomUser(id=id,email_id=data.email_id,phone_number=phone_number,password=data.password,restaurant_name=rname,restaurant_logo=rlogo,restaurant_address=address,payment_status=data.payment_status,payment_price=data.payment_price,package=data.package,subscritpion_expire_date=data.subscritpion_expire_date,subscription_date=data.subscription_date).save()
        else:
            CustomUser(id=id,email_id=data.email_id,phone_number=phone_number,password=data.password,restaurant_name=rname,restaurant_logo=data.restaurant_logo,restaurant_address=address,payment_status=data.payment_status,payment_price=data.payment_price,package=data.package,subscritpion_expire_date=data.subscritpion_expire_date,subscription_date=data.subscription_date).save()
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
            data = CustomUser.objects.get(id=id)
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
                print(data.payment_diable_enable_status)
                
                return render(request, 'admin/users/edit_admin.html', {'datas': data})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login ')
    def post(self, request, id):
        full_name=request.POST.get('full_name')
        restaurant_logo=request.FILES.get('restaurant_logo')
        phone_number=request.POST.get('phone_number')
        email_id=request.POST.get('email_id')
        data=CustomUser.objects.get(id=id)
        print(restaurant_logo)
        if restaurant_logo:
            print('image')
            data.restaurant_logo=restaurant_logo
        data.full_name=full_name
        data.phone_number=phone_number
        data.email_id=email_id
        data.save()

        messages.success(request,'Update Succesfully!!!')
        return redirect('admin-dashboard')

class Payment_enable_diable(View):
    def post(self,request):
        data=CustomUser.objects.get(id=request.POST.get('id'))
        if data.payment_diable_enable_status == 'False':
            data.payment_diable_enable_status="True"
            data.save()
        else:
            print('datya')
            data.payment_diable_enable_status ="False"
            data.save()
        return redirect('edit-admin',data.id)

class User_Payment(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser is True:
                data=CustomUser.objects.filter(is_admin=False).order_by('restaurant_name')
                return render(request,'admin/payment.html',{'data':data})
            else:
                messages.error(request,'You are not admin')
                return redirect('user-login')
        else:
            return redirect('admin-login')


# class Add_SubscriptionsDetails(View):
#     def get(self,request):
#         if request.user.is_authenticated:
#             if request.user.is_superuser is True:
#                 return render(request,'admin/subscription_details/add_subscription_details.html')
#             else:
#                 messages.error(request,'You are not admin')
#                 return redirect('user-login')
#         else:
#             return redirect('admin-login')
    
#     def post(self,request):
#         heading=request.POST.get('heading')
#         subscription_price=request.POST.get('subscription_price')
#         subscription_duration=request.POST.get('subscription_duration')
#         SubscriptionDetails.objects.create(heading=heading,subscription_duration=subscription_duration,subscription_price=subscription_price)
#         return redirect('show-subscription')

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

# def delete_subscriptionsdetails(request,id):
#     if request.user.is_superuser is True:
#         if request.method=='POST':
#             data=SubscriptionDetails.objects.get(id=id)
#             data.delete()
#         return redirect('show-subscription')
#     else:
#             messages.error(request,'You are not admin')
#             return redirect('user-login')

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
            users = Notification.objects.all()

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
        

class Termsandconditions_add(View):
    def get(self,request):
        if  request.user.is_authenticated:
            return render(request,'admin/termandcondition/termandcom_add.html')
        else:
            return redirect('admin-login')
        
    def post(self,request):
        description=request.POST.get('description')
        img=request.FILES.get('img')

        Termandcondition.objects.create(img=img,description=description)
        return redirect('show-termandcondition')

class Termsandconditions_show(View):
    def get(self,request):
        if  request.user.is_authenticated:
            users = Termandcondition.objects.all().order_by('-id')
            return render(request,'admin/termandcondition/termandcon_view.html',{'Users':users})
        else:
            return redirect('admin-login')


class Termsandconditions_Edit(View):
    def get(self, request, id):
        if  request.user.is_authenticated:
            data = Termandcondition.objects.get(pk=id)
        
            
            return render(request, 'admin/termandcondition/termandcon_edit.html', {'datas': data})
        else:
            return redirect('admin-login')
        


    def post(self, request, id):
        data = Termandcondition()
        img=request.FILES.get('img')
        description=request.POST.get('description')
        data = Termandcondition.objects.get(id=id)
        if img is not None:
            Termandcondition(id=id,description=description, img=img,created_at=data.created_at).save()
        else:
            Termandcondition(id=id,description=description, img=data.img,created_at=data.created_at).save()

        return redirect('show-termandcondition')


def delete_Termsandconditions(request ,id):
        if request.method=='POST':
            pi=Termandcondition.objects.get(pk=id)
            pi.delete()
        return redirect('show-termandcondition')




class Privacyandpolicy_add(View):
    def get(self,request):
        if  request.user.is_authenticated:
            return render(request,'admin/privcayandpolicy/privacyandpolicy_add.html')
        else:
            return redirect('admin-login')
        
    def post(self,request):
        img=request.FILES.get('img')
        description=request.POST.get('description')

        PrivacyAndPolicy.objects.create(img=img,description=description)
        return redirect('show-privacyandpolicy')

class Privacyandpolicy_show(View):
    def get(self,request):
        if  request.user.is_authenticated:
            users = PrivacyAndPolicy.objects.all().order_by('-id')
            return render(request,'admin/privcayandpolicy/privacyandpolicy_view.html',{'Users':users})
        else:
            return redirect('admin-login')


class Privacyandpolicy_Edit(View):
    def get(self, request, id):
        if  request.user.is_authenticated:
            data = PrivacyAndPolicy.objects.get(pk=id)
            
            return render(request, 'admin/privcayandpolicy/privacyandpolicy_edit.html', {'datas': data})
        else:
            return redirect('admin-login')
        


    def post(self, request, id):
        data = PrivacyAndPolicy()
        img=request.FILES.get('img')

        description=request.POST.get('description')
        data = PrivacyAndPolicy.objects.get(id=id)
        if img is not None:
            PrivacyAndPolicy(id=id,img=img,description=description, created_at=data.created_at).save()
        else:
            PrivacyAndPolicy(id=id,img=data.img,description=description, created_at=data.created_at).save()

        return redirect('show-privacyandpolicy')


def delete_Privacyandpolicy(request ,id):
        if request.method=='POST':
            pi=PrivacyAndPolicy.objects.get(pk=id)
            pi.delete()
        return redirect('show-privacyandpolicy')



class Show_Menu_Categories(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data=FoodCategories.objects.filter(user_id=id)
            return render(request,'admin/menu/categories/show_category.html',{'data':data})

        else:
            return redirect('admin-login')
        
class Edit_Menu_Categories(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data=FoodCategories.objects.get(id=id)
            return render(request,'admin/menu/categories/edit_category.html',{'data':data})

        else:
            return redirect('admin-login')
        
   
    def post(self,request,id):
        category_name=request.POST.get('category_name')
        data=FoodCategories.objects.get(id=id)
        FoodCategories(id=id,category_name=category_name,created_at=data.created_at,user_id=data.user_id,).save()
        return redirect('menu-details',data.user_id.id )
    
def delete_category(request,id):
    if request.user.is_authenticated:
            data=FoodCategories.objects.get(id=id)
            data.delete()
            return redirect('menu-details',data.user_id.id )

    else:
        return redirect('admin-login')
    

class Show_Menu_food_items(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data=FoodName.objects.filter(category_name=id)
            return render(request,'admin/menu/items/show_items.html',{'data':data})
            

        else:
            return redirect('admin-login')
        

class Edit_Menu_food_items(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data=FoodName.objects.get(id=id)
            return render(request,'admin/menu/items/edit_items.html',{'data':data})
        else:
            return redirect('admin-login')
        
    def post(self,request,id):
        data=FoodName.objects.get(id=id)
        food_name=request.POST.get('food_name')
        food_image=request.FILES.get('food_image')
        full_price=request.POST.get('full_price')
        medium_price=request.POST.get('medium_price')
        small_price=request.POST.get('small_price')
        if food_image is not None:
            FoodName(id=id,category_name=data.category_name,food_name=food_name,food_image=food_image,full_price=full_price,medium_price=medium_price,small_price=small_price,created_at=data.created_at,user_id=data.user_id).save()
        else:
            FoodName(id=id,category_name=data.category_name,food_name=food_name,food_image=data.food_image,full_price=full_price,medium_price=medium_price,small_price=small_price,created_at=data.created_at,user_id=data.user_id).save()
        return redirect('show-menu-food',data.category_name.id)
    

def delete_item(request,id):
    if request.user.is_authenticated:
            data=FoodName.objects.get(id=id)
            data.delete()
            return redirect('show-menu-food',data.category_name.id )

    else:
        return redirect('admin-login')
    


class Add_Category_Image(View):
    def get(self,request):
        if request.user.is_authenticated:
                return render(request,'admin/catimage/addimage.html')
        else:
            return redirect('admin-login')
    def post(self,request):
        image=request.FILES.getlist('image')
        for image in image:
            CategoryImages.objects.create(image=image)
        return redirect('show-image')
    

class Show_Category_Image(View):
    def get(self,request):
        if request.user.is_authenticated:
                data=CategoryImages.objects.all().order_by('-id')
                return render(request,'admin/catimage/showimage.html',{'data':data})
        else:
            return redirect('admin-login')
        

class Edid_Category_Image(View):
    def get(self,request,id):
        if request.user.is_authenticated:
                data=CategoryImages.objects.get(id=id)
                return render(request,'admin/catimage/editimage.html',{'data':data})
        else:
            return redirect('admin-login')
    def post(self,request,id):
        data=CategoryImages.objects.get(id=id)
        image=request.FILES.get('image')
        if image:
            data.image=image
            data.save()
        return redirect('show-image')
    
def deleteimage(request,id):
    if request.user.is_authenticated:
        data=CategoryImages.objects.get(id=id).delete()
        return redirect('show-image')
    else:
        return redirect('admin-login')