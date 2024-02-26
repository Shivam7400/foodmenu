from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.contrib.auth import login , logout ,authenticate
from django.contrib.auth.decorators import login_required
from Adminapp.models import *
from .models import *
from django.contrib import messages
import razorpay
from foodmenu.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
from django.template.loader import get_template
from xhtml2pdf import pisa



# Create your views here.
class User_Login(View):
    
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request,'restaurent_admin/login.html')
        else:
            if  RestaurentDetails.objects.filter(payment_status='Successfull',user_id=request.user).exists():
                return redirect('user-dashboard')
            elif  RestaurentDetails.objects.filter(payment_status='pending',user_id=request.user).exists():
                return redirect('subscription')
            else: 
                return redirect('add-restaurant-details')
            

    def post(self,request):
        email_id=request.POST.get('email_id') 
        passwords=request.POST.get('password')
        print(email_id,passwords,"jfjkfdf")
        user = authenticate(
                request=request, email_id=email_id, password=passwords,)
        print(user,'user')
        if user is not None:
            if CustomUser.objects.filter(email_id=email_id, is_superuser=False):
                login(request, user)
                if RestaurentDetails.objects.filter(payment_status='Successfull',user_id=request.user).exists():
                    return redirect('user-dashboard')
                elif RestaurentDetails.objects.filter(payment_status='pending',user_id=request.user).exists():
                    return redirect('subscription')
                else:
                    return redirect('add-restaurant-details')
            else:
                messages.warning(request, 'You Are Not User')
        else:
            messages.warning(request, 'Invalid Email or Password')
        return redirect('user-login')
    
class UserDashboard(View):
    def get(self,request):
        
        if request.user.is_authenticated:
            if RestaurentDetails.objects.filter(user_id=request.user).exists():
                category=FoodCategories.objects.filter(user_id=request.user).all().count()
                item=FoodName.objects.all().filter(user_id=request.user).count()
                noti=Notification.objects.all().filter(receiver=request.user).count()
                
                return render(request,'restaurent_admin/dashboard.html',{'category':category,'item':item,'noti':noti})
            else:
                return redirect('add-restaurant-details')
        else:        
            return redirect('user-login')
        


def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Log Out Successfully')
        return redirect('user-login')

    else:
        return redirect('user-login')
    
class Change_password(View):
    
    def get(self, request):
        if  request.user.is_authenticated:
            return render(request, 'restaurent_admin/password_reset.html')
        else:
            return redirect('user-dashboard') 
    def post(self, request):
        id=request.user.id
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        
        if new_password == confirm_password:
            new_password = confirm_password
            user = CustomUser.objects.get(id=id)
            check=user.check_password(old_password)
        
            if check==True:
                user.set_password(new_password)
                user.save()
                
                messages.success(request, 'New password  Successfully..!!')
                return redirect("user-dashboard")
            else:

                messages.error(request, 'Incorrect Old Password..!!')
        else:
            messages.warning(request, 'please check your newpassword and confirm password..!!')
     
        return redirect('change-user-password')

class UserRegistration(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request,'restaurent_admin/registration.html')
        else:
            return redirect('user-login')
        
    def post(self,request):
        full_name=request.POST.get('full_name')
        choose_profilepic=request.FILES.get('choose_profilepic')
        email_id=request.POST.get('email_id')
        password=request.POST.get('password')
        phone_number=request.POST.get('phone_number')
        print(choose_profilepic,full_name,'pic')
        CustomUser.objects.create_user(full_name=full_name,choose_profilepic=choose_profilepic,email_id=email_id,password=password,phone_number=phone_number)
        return redirect('user-login')
    
class Edit_Users_Profile(View):
    def get(self, request, id):
        if  request.user.is_authenticated:
            data = CustomUser.objects.get(pk=id)
            return render(request, 'restaurent_admin/edit-user-profile.html', {'datas': data})
        else:
            return redirect('user-login')
    def post(self, request, id):
        data=CustomUser()
        choose_profilepic=request.FILES.get('choose_profilepic')
        full_name=request.POST.get('full_name')
        phone_number=request.POST.get('phone_number')
        if choose_profilepic is not None:
            
            data=CustomUser(id=id,choose_profilepic=choose_profilepic,email_id=request.user.email_id,full_name=full_name,phone_number=phone_number,password=request.user.password).save()
        else:
            data =CustomUser.objects.get(pk=id)
            data=CustomUser(id=id,choose_profilepic=data.choose_profilepic,email_id=request.user.email_id,full_name=full_name,phone_number=phone_number,password=request.user.password).save()
        messages.success(request,'Profile Update Successfully!!!')
        return redirect('user-dashboard')



class Add_Category(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data=RestaurentDetails.objects.get(id=id)
            return render(request,'restaurent_admin/add_categories/add_catergory.html',{'data':data})
        else:
            return redirect('user-login')
    def post(self,request,id):
        restaurant_id=RestaurentDetails.objects.get(id=id)
        category_name=request.POST.get('category_name')
        FoodCategories.objects.create(category_name=category_name,restaurant_id=restaurant_id,user_id=request.user)
        return redirect('show-category')
    
class Show_Category(View):
    def get(self,request):
        if request.user.is_authenticated:
            id=request.user
            if RestaurentDetails.objects.filter(user_id=id).exists():
                restaurant_id=RestaurentDetails.objects.get(user_id=id)
                data=FoodCategories.objects.all().filter(restaurant_id=restaurant_id)
                return render(request,'restaurent_admin/add_categories/show_category.html',{'data':data,'restaurant_id':restaurant_id})
            else:
                
                return redirect('add-restaurant-details')
        else:
            return redirect('user-login')
    
class Edit_Category(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data=FoodCategories.objects.get(id=id)
            return render(request,'restaurent_admin/add_categories/edit_category.html',{'data':data})
        else:
            return redirect('user-login')
    def post(self,request,id):
        category_name=request.POST.get('category_name')
        data=FoodCategories.objects.get(id=id)
        FoodCategories(id=id,category_name=category_name,created_at=data.created_at,user_id=data.user_id,restaurant_id=data.restaurant_id).save()
        messages.success(request,'Update Successfully!!!')
        return redirect('show-category')

def delete_category(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            data=FoodCategories.objects.get(id=id)
            new=RestaurentDetails.objects.get(id=data.restaurant_id.id)
        print(new)
        data.delete()
        return redirect('show-category')
    else:
        return redirect('user-login')
    

class Add_Item(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data=FoodCategories.objects.get(id=id)
            print(data,'data')
            return render(request,'restaurent_admin/add_items/add_item.html',{'data':data})
        else:
            return redirect('user-login')
    def post(self,request,id):
        data=FoodCategories.objects.get(id=id)
        category_name=data
        food_name=request.POST.get('food_name')
        food_image=request.FILES.get('food_image')
        full_price=request.POST.get('full_price')
        medium_price=request.POST.get('medium_price')
        small_price=request.POST.get('small_price')
        FoodName.objects.create(food_name=food_name,food_image=food_image,full_price=full_price,medium_price=medium_price,small_price=small_price,category_name=category_name,user_id=request.user)
        return redirect('show-category')
    
class Show_Item(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data=FoodCategories.objects.get(id=id)
            item=FoodName.objects.all().filter(category_name=data.id).order_by('food_name')
            return render(request,'restaurent_admin/add_items/show_item.html',{'item':item,'data':data})

        else:
            return redirect('user-login')
        

class Edit_Item(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data=FoodName.objects.get(id=id)
            return render(request,'restaurent_admin/add_items/edit_item.html',{'data':data})
        else:
            return redirect('user-login')
    def post(self,request,id):
        data=FoodName.objects.get(id=id)
        food_name=request.POST.get('food_name')
        food_image=request.FILES.get('food_image')
        full_price=request.POST.get('full_price')
        medium_price=request.POST.get('medium_price')
        small_price=request.POST.get('small_price')
        if food_image is not None:
            FoodName(id=id,category_name=data.category_name,food_name=food_name,food_image=food_image,full_price=full_price,medium_price=medium_price,small_price=small_price,created_at=data.created_at,user_id=request.user).save()
        else:
            FoodName(id=id,category_name=data.category_name,food_name=food_name,food_image=data.food_image,full_price=full_price,medium_price=medium_price,small_price=small_price,created_at=data.created_at).save()
        messages.success(request,'Update Successfully!!!')
        return redirect('show-item',data.category_name.id)

def delete_item(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            data=FoodName.objects.get(id=id)
            data.delete()
        return redirect('show-item',data.category_name.id)

    else:
        return redirect('user-login')


class Add_Restaurant_Deltails(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request,'restaurent_admin/restaurant_details/add_restaurent.html')
        else:
            return redirect('user-login')
    def post(self,request):
        restaurant_name=request.POST.get('restaurant_name')
        restaurant_id=request.POST.get('restaurant_id')
        restaurant_address=request.POST.get('restaurant_address')

        if RestaurentDetails.objects.filter(user_id=request.user).exists():
            if not RestaurentDetails.objects.filter(restaurant_id=restaurant_id).exists():

                RestaurentDetails.objects.create(restaurant_address=restaurant_address,restaurant_name=restaurant_name,restaurant_id=restaurant_id,user_id=request.user)
                return redirect('subscription')
            else:
                messages.warning(request,'Id already Exist')
                return redirect('add-restaurant-details')
        else:
            if not RestaurentDetails.objects.filter(restaurant_id=restaurant_id).exists():

                RestaurentDetails.objects.create(restaurant_address=restaurant_address,restaurant_name=restaurant_name,restaurant_id=restaurant_id,user_id=request.user)
                return redirect('subscription')
            else:
                messages.warning(request,'Id already Exist')
                return redirect('add-restaurant-details')
        
class Show_Restaurant_Details(View):
    def get(self,request):
        if request.user.is_authenticated:
            id=request.user
            print(id,"id")
            if RestaurentDetails.objects.filter(user_id=id).exists():
                data=RestaurentDetails.objects.all().filter(user_id=id)
                print(data)
                return render(request,'restaurent_admin/restaurant_details/show_restaurent.html',{'data':data})
            else:
                print("ksfsd")
                return redirect('add-restaurant-details')

        else:
            return redirect('user-login')
        


class Edit_Restaurant_Details(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data=RestaurentDetails.objects.get(id=id)
            return render(request,'restaurent_admin/restaurant_details/edit_restaurent.html',{'data':data})
        else:
            return redirect('user-login')
    def post(self,request,id):
        data=RestaurentDetails.objects.get(id=id)
        restaurant_name=request.POST.get('restaurant_name')
        restaurant_id=request.POST.get('restaurant_id')
        restaurant_address=request.POST.get('restaurant_address')
        RestaurentDetails(id=id,restaurant_address=restaurant_address,restaurant_name=restaurant_name,restaurant_id=restaurant_id,user_id=data.user_id,payment_status=data.payment_status).save()
        messages.success(request,'Update Successfully!!!')
        return redirect('show-restaurant-details')


def delete_restaurant_details(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            data=RestaurentDetails.objects.get(id=id)
            data.delete()
        return redirect('show-restaurant-details')
    else:
            return redirect('user-login')



class Restaurant_details(View):
    def get(self,request,id):
      
        data=RestaurentDetails.objects.get(id=id)
        print(data.id,'name')
        return render(request,'restaurent_admin/restaurant_details/restaurant_profile.html',{'data':data})


class HomePage(View):
    def get(self,request):
        if request.user.is_authenticated:
            id=request.user
            print(id,"id")
            data=RestaurentDetails.objects.all().filter(user_id=id)
            return render(request,'restaurent_admin/home.html',{'data':data})
        else:
            return redirect('user-login')



class Restaurant_Menu(View):
    def get(self,request,menu):
        print(menu,'menu')
        if RestaurentDetails.objects.filter(restaurant_name=menu).exists():
            print('dssdff')
            idd=RestaurentDetails.objects.get(restaurant_name=menu)
            if idd.is_active is True:
        
                catagory=FoodCategories.objects.filter(restaurant_id=idd)
                
                return render(request,'restaurent_admin/restaurent_menu.html', {'category':catagory,'idd':idd} )
            else:
                return HttpResponse("<h1>Page Not Found......<h1>")
        else:
            return HttpResponse("<h1>bad request...<h1>")

class User_Subscription(View):
    
    def get(self,request):
        client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        order_amount= 10000000
        order_currency= "INR"
        payment_order=client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture=1))
        payment_order_id=payment_order['id']
        data=SubscriptionDetails.objects.all()
        return render(request,'restaurent_admin/subscription.html',{'data':data,'api_key':RAZORPAY_API_KEY,'order_id':payment_order_id})
    def post(self,request):
        id=request.user
        data=RestaurentDetails.objects.get(user_id=id)
        payment=request.POST.get('payment')
        if data.payment_status == 'pending':
            data.payment_status='Successfull'
            RestaurentDetails(id=data.id,restaurant_address=data.restaurant_address,restaurant_name=data.restaurant_name,restaurant_id=data.restaurant_id,user_id=data.user_id,payment_status=data.payment_status,payment_price=payment).save()
            return redirect('user-dashboard')
        else:
            pass
        

class Receive_Notification(View):
    def get(self,request):
        if request.user.is_authenticated:
            id=request.user
            data=Notification.objects.all().filter(receiver=id)
            return render(request,'restaurent_admin/notification.html',{'data':data})
        else:
            return redirect('user-login')

def delete_notification(request,id):
    if request.method=='POST':
        data=Notification.objects.get(id=id)
        data.delete()
    return redirect('receive-notification')


def generate_pdf(request,id):
    # Create a new PDF object
    data=RestaurentDetails.objects.get(id=id)
    template = get_template('restaurent_admin/restaurant_details/my_template.html')
    html = template.render({'data': data})

    # Convert HTML to PDF
    pdf_file = open('my_pdf_file.pdf', 'w+b')
    pisa_status = pisa.CreatePDF(html.encode('utf-8'), dest=pdf_file)

    # Return the PDF as a response
    if pisa_status.err:
        return HttpResponse('Error generating PDF file')
    else:
        pdf_file.seek(0)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="my_pdf_file.pdf"'
        return response