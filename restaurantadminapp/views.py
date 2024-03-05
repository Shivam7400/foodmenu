from django.shortcuts import render,redirect,HttpResponse 
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import login , logout ,authenticate
from Adminapp.models import *
from .models import *
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date , timedelta
import json


#sideBar


# Create your views here.
class User_Login(View):
    
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request,'restaurent_admin/login.html')
        else:
            if  CustomUser.objects.filter(payment_status='Successfull',id=request.user.id).exists():
                return redirect('user-dashboard')
            else:
                return redirect('subscription')
    def post(self,request):
        email_id=request.POST.get('email_id') 
        passwords=request.POST.get('password')
        
        user = authenticate(
                request=request, email_id=email_id, password=passwords,)
        print(user,'user')
        if user is not None:
            if CustomUser.objects.filter(email_id=email_id, is_superuser=False):
                login(request, user)
                if CustomUser.objects.filter(payment_status='Successfull',id=request.user.id).exists():
                    return redirect('user-dashboard')
                else:
                    return redirect('subscription')
            else:
                messages.warning(request, 'You Are Not User')
        else:
            messages.warning(request, 'Invalid Email or Password')
        return redirect('user-login')
    
class UserDashboard(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser is False:
                data1=CustomUser.objects.get(id=request.user.id) 
                if data1.payment_status=='Successfull':
                    time=date.today()
                    newt=str(time)
                    print(newt)
                    if newt > data1.subscritpion_expire_date:
                        data1.payment_status='pending'
                        data1.save()              
                if CustomUser.objects.filter(payment_status='Successfull',id=request.user.id).exists():
                    cat=FoodCategories.objects.filter(user_id=request.user)
                    category=cat.count()
                    item=FoodName.objects.all().filter(user_id=request.user).count()
                    noti=Notification.objects.all().filter(receiver=request.user,read=False).count()
                    cat_image=CategoryImages.objects.all()
                    
                    return render(request,'restaurent_admin/dashboard.html',context= {'category':category,'item':item,'noti':noti,'rname':data1,'cat':cat,'cat_image':cat_image})
                else:
                    print('hello')
                    return redirect('subscription')

            else:
                return redirect('adminlogin')
            
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
            data1=CustomUser.objects.get(id=request.user.id)
            time=date.today()
            newt=str(time)
            if newt > data1.subscritpion_expire_date:
                data1.payment_status='pending'
                data1.save()
                return redirect('subscription')
            else:
                return render(request, 'restaurent_admin/change_password.html',{'rname':data1})
        else:
            return redirect('user-dashboard') 
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
            
            messages.success(request, 'Password Change Successfully..!!')
            return redirect("user-dashboard")
        else:

            messages.error(request, 'Incorrect Old Password..!!')
    
        return redirect('change-user-password')

class UserRegistration(View):
    def get(self,request):
        if not request.user.is_authenticated:
            
            return render(request,'restaurent_admin/registration.html')
        else:
            return redirect('user-login')
        
    def post(self,request):
        rname=request.POST.get('Rname')
        rlogo=request.FILES.get('Rlogo')
        email_id=request.POST.get('email_id')
        password=request.POST.get('password')
        address=request.POST.get('address')
        phone_number=request.POST.get('phone_number')
        print(rlogo,'logo')
        print(rname,'logo')
        print(phone_number,'phone')
        if not CustomUser.objects.filter(email_id=email_id).exists():
            CustomUser.objects.create_user(email_id=email_id,password=password,phone_number=phone_number,restaurant_name=rname,restaurant_logo=rlogo,restaurant_address=address)

            messages.success(request,'Account create Successfully!!!')
            return redirect('user-login')
        else:
            messages.warning(request,'Email Alreday exists!!!')
            return redirect('user-registration')
        


    

# class HomePage(View):
#     def get(self,request):
#         if not request.user.is_authenticated:
#             return render(request,'restaurent_admin/homepage.html')
#         else:
#             if request.user.is_superuser is False:
#                 return redirect('user-dashboard')
#             else:
#                 return redirect('admin-dashboard')

        
# class Edit_Users_Profile(View):
#     def get(self, request, id):
#         if  request.user.is_authenticated:
#             data = CustomUser.objects.get(pk=id)
#             return render(request, 'restaurent_admin/edit-user-profile.html', {'datas': data})
#         else:
#             return redirect('user-login')
#     def post(self, request, id):
#         data=CustomUser()
#         choose_profilepic=request.FILES.get('choose_profilepic')
#         full_name=request.POST.get('full_name')
#         phone_number=request.POST.get('phone_number')
#         deletepic=request.POST.get('deletepic')
#         if choose_profilepic and deletepic:
#             messages.warning(request,'Either Select Add Picture or Remove Picture')
#             return redirect('edit-users-profile', id)
#         else:
#             if deletepic is None:
#                 if choose_profilepic is not None:
                    
#                     data=CustomUser(id=id,choose_profilepic=choose_profilepic,email_id=request.user.email_id,full_name=full_name,phone_number=phone_number,password=request.user.password).save()
#                 else:
#                     data =CustomUser.objects.get(pk=id)
#                     data=CustomUser(id=id,choose_profilepic=data.choose_profilepic,email_id=request.user.email_id,full_name=full_name,phone_number=phone_number,password=request.user.password).save()
#                 messages.success(request,'Profile Update Successfully!!!')
#                 return redirect('user-dashboard')
#             else:
#                 print('True')
#                 data =CustomUser.objects.get(pk=id)
            
#                 data=CustomUser(id=id,email_id=request.user.email_id,full_name=full_name,phone_number=phone_number,password=request.user.password).save()

#                 return redirect('user-dashboard')

class Add_Category(View):
    def post(self,request):
        category_name=request.POST.get('category_name')
        category_image=request.POST.get('category_image')
        print(category_image,'asdhas')
        if category_image != '':
            data=CategoryImages.objects.get(id=category_image)
            FoodCategories.objects.create(category_name=category_name,category_image=data.image ,user_id=request.user)
        else:
            FoodCategories.objects.create(category_name=category_name,user_id=request.user)
        messages.success(request,'Category has been created')
        return redirect('user-dashboard')
    
class Show_Category(View):
    def get(self,request):
        if request.user.is_authenticated:
            data1=CustomUser.objects.get(id=request.user.id)
            time=date.today()
            newt=str(time)
            if newt > data1.subscritpion_expire_date:
                data1.payment_status='pending'
                data1.save()
                return redirect('subscription')
            else:
                data=FoodCategories.objects.filter(user_id=data1)
                return render(request,'restaurent_admin/add_categories/show_category.html',{'data':data,'rname':data1})

        else:
            return redirect('user-login')
    
class Edit_Category(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data1=CustomUser.objects.get(id=request.user.id)
            time=date.today()
            newt=str(time)
            if newt > data1.subscritpion_expire_date:
                data1.payment_status='pending'
                data1.save()
                return redirect('subscription')
            else:
                data=FoodCategories.objects.get(id=id)
                return render(request,'restaurent_admin/add_categories/edit_category.html',{'data':data,'rname':data1})
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
            data.delete()
        return redirect('show-category')
    else:
        return redirect('user-login')
    

class Add_Item(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            cat=FoodCategories.objects.get(id=id)
            data1=CustomUser.objects.get(id=cat.user_id.id)
            time=date.today()
            newt=str(time)
            if newt > data1.subscritpion_expire_date:
                data1.payment_status='pending'
                data1.save()
                return redirect('subscription')
            else:
                categories=FoodCategories.objects.filter(user_id=request.user).exclude(id=cat.id)
                return render(request,'restaurent_admin/add_items/add_item.html',{'rname':data1,'cat':cat,'categories':categories})
        else:
            return redirect('user-login')
    def post(self,request,id):
        print('hello')
        
        food_name=request.POST.get('food_name')
        food_image=request.FILES.get('food_image')
        price=request.POST.get('price')
        description=request.POST.get('description')
        button=request.POST.get('submit_button')
        category=request.POST.get('category')
        data=FoodCategories.objects.get(id=category)
        print(button)
        if button=='publish':
            status='Publish'
        else:
            status='Save'
            print(food_name)
        name=FoodName.objects.create(food_name=food_name,food_image=food_image,price=price,description=description,category_name=data,user_id=request.user,status=status)
        return redirect('edit-item',name.id)
    

class Add_Once(View):
    def post(self,request,id):
        print('hello')
        fname =FoodName.objects.get(id=id)
        name=request.POST.get('addname')
        price=request.POST.get('addprice')
        print(price)
        AddOnes.objects.create(name=name,price=price,user_id=request.user,foodname=fname)
        return redirect('edit-item',fname.id)
    
class Delete_Add_Once(View):
    def get(self,request,id):
        a=AddOnes.objects.get(id=id)
        fname =FoodName.objects.get(id=a.foodname.id)
        a.delete()
        return redirect('edit-item',fname.id)
from django.urls import reverse
class Show_Item(View):
    def get(self,request,id):
        if request.user.is_authenticated:   
            
            data1=CustomUser.objects.get(id=request.user.id)
            time=date.today()
            newt=str(time)
            if newt > data1.subscritpion_expire_date:
                data1.payment_status='pending'
                data1.save()
                return redirect('subscription')
            else:
                data=FoodCategories.objects.get(id=id)
                item=FoodName.objects.all().filter(category_name=data.id,user_id=request.user,status='Publish').order_by('food_name')
                
                return render(request,'restaurent_admin/add_items/show_item.html',{'item':item,'data':data,'rname':data1})
        else:
            return redirect('user-login')
        
    def post(self,request,id):
        item_id=request.POST['cat_id']
        items=FoodName.objects.get(id=item_id)
        print(items)
        addonce=AddOnes.objects.filter(foodname=items)
        dataa = list(addonce.values())
        print(dataa)
        src="/media/"+str(items.food_image)
        url = "http://127.0.0.1:8000/edit-item/"+str(items.id)
        print(url)
        context={'id':items.id,'name':items.food_name,'description':items.description,'image':str(items.food_image),'price':items.price,'image':src,'url':url,'data':dataa}
        return JsonResponse(context)
        

class Edit_Item(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            data1=CustomUser.objects.get(id=request.user.id)
            time=date.today()
            newt=str(time)
            if newt > data1.subscritpion_expire_date:
                data1.payment_status='pending'
                data1.save()
                return redirect('subscription')
            else:
                
                data=FoodName.objects.get(id=id)
                category=FoodCategories.objects.filter(user_id=request.user).exclude(id=data.category_name.id)
                addone=AddOnes.objects.filter(user_id=request.user,foodname=data)
                return render(request,'restaurent_admin/add_items/edit_item.html',{'data':data,'rname':data1,'addone':addone,'category':category})
        else:
            return redirect('user-login')
    def post(self,request,id):
        data=FoodName.objects.get(id=id)
        food_name=request.POST.get('food_name')
        food_image=request.FILES.get('food_image')
        price=request.POST.get('price')
        description=request.POST.get('description')
        button=request.POST.get('submit_button')
        category=request.POST.get('category')
        if button == 'publish':
            status='Publish'
        else:
            status="Save"
        if food_image is not None:
            data.food_image=food_image
        data.food_name=food_name
        data.description=description
        data.status=status
        data.price=price
        data.category_name=FoodCategories.objects.get(id=category)
        data.save()
        messages.success(request,'Update Successfully!!!')
        if button == 'publish':
            return redirect('show-item',data.category_name.id)
        else:
            return redirect('show-all-item')
        

def delete_item(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            data=FoodName.objects.get(id=id)
            data.delete()
        return redirect('show-item',data.category_name.id)

   
class Delete_item(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.GET.getlist('checkid')
            cat_id = request.GET['cat_id']
            data_list = json.loads(user_id[0])
            data=FoodName.objects.filter(id__in=data_list)
            data.delete()
            if cat_id=="hello":
                return redirect('show-all-item')
            else:
                return redirect('show-item',cat_id)
        else:
            return redirect('user-login')
        
class Show_all_items(View):
    def get(self,request):
        if request.user.is_authenticated:
            data1=CustomUser.objects.get(id=request.user.id)
            time=date.today()
            newt=str(time)
            if newt > data1.subscritpion_expire_date:
                data1.payment_status='pending'
                data1.save()
                return redirect('subscription')
            else:
                data=FoodName.objects.filter(user_id=request.user,status='Save').order_by('food_name')
                return render(request,'restaurent_admin/add_items/all_items.html',{'data':data})
        else:
            return redirect('user-login')

    
class Add_Item_all(View):
    def get(self,request):
        if request.user.is_authenticated:
            data1=CustomUser.objects.get(id=request.user.id)
            time=date.today()
            newt=str(time)
            if newt > data1.subscritpion_expire_date:
                data1.payment_status='pending'
                data1.save()
                return redirect('subscription')
            else:
                data=FoodCategories.objects.filter(user_id=data1.id)
                return render(request,'restaurent_admin/add_items/add_all_items.html',{'data':data})
        else:
            return redirect('user-login')
    def post(self,request):
        food_name=request.POST.get('food_name')
        food_image=request.FILES.get('food_image')
        price=request.POST.get('price')
        description=request.POST.get('description')
        button=request.POST.get('submit_button')
        category=request.POST.get('category')
        data=FoodCategories.objects.get(id=category)
        print(button)
        if button=='publish':
            status='Publish'
        else:
            status='Save'
            print(food_name)
        name=FoodName.objects.create(food_name=food_name,food_image=food_image,price=price,description=description,category_name=data,user_id=request.user,status=status)
        return redirect('edit-item',name.id)


class Restaurant_details(View):
    def get(self,request):
        if request.user.is_authenticated:
            data1=CustomUser.objects.get(id=request.user.id)
            time=date.today()
            newt=str(time)
            if newt > data1.subscritpion_expire_date:
                data1.payment_status='pending'
                data1.save()
                return redirect('subscription')
            else:
                return render(request,'restaurent_admin/restaurant_details/restaurant_profile.html',{'rname':data1})
        else:
            return redirect('user-login')
        
    def post(self,request):
        print(id,'id')
        rname=request.POST.get('restaurant_name')
        rlogo=request.FILES.get('restaurant_logo')
        address=request.POST.get('restaurant_address')
        phone_number=request.POST.get('phone_number')
        data=CustomUser.objects.get(id=request.user.id)
        print(rname,rlogo,address)
        if rlogo is not None:
            CustomUser(id=data.id,email_id=data.email_id,phone_number=phone_number,password=request.user.password,restaurant_name=rname,restaurant_logo=rlogo,restaurant_address=address,payment_status=data.payment_status,payment_price=data.payment_price,package=data.package,subscritpion_expire_date=data.subscritpion_expire_date,subscription_date=data.subscription_date).save()
        else:
            CustomUser(id=data.id,email_id=data.email_id,phone_number=phone_number,password=request.user.password,restaurant_name=rname,restaurant_logo=data.restaurant_logo,restaurant_address=address,payment_status=data.payment_status,payment_price=data.payment_price,package=data.package,subscritpion_expire_date=data.subscritpion_expire_date,subscription_date=data.subscription_date).save()
        messages.success(request,'Profile Updated!!')
        return redirect('user-dashboard')
    




# class Restaurant_Menu(View):
#     def get(self,request,id):
#         if RestaurentDetails.objects.filter(user_id=int(id)).exists():
#             idd=RestaurentDetails.objects.get(user_id=int(id))
#             print(idd.payment_status)
#             if idd.payment_status != 'pending':
        
#                 catagory=FoodCategories.objects.filter(restaurant_id=idd)
                
#                 return render(request,'restaurent_admin/restaurent_menu.html', {'category':catagory,'idd':idd} )
#             else:
#                 return HttpResponse("<h1>Page Not Found......<h1>")
#         else:
#             return HttpResponse("<h1>bad request...<h1>")
        




class User_Subscription(View):
    
    def get(self,request):
        if request.user.is_authenticated:
            
            if CustomUser.objects.filter(payment_status='pending',id=request.user.id).exists():
                name=CustomUser.objects.get(id=request.user.id)
                standard=SubscriptionDetails.objects.get(heading='Standard')
                basic=SubscriptionDetails.objects.get(heading='Basic')
                premium=SubscriptionDetails.objects.get(heading='Premium')
                
                return render(request,'restaurent_admin/subscription.html',{'standard':standard,'basic':basic,'premium':premium,'name':name})
                # return render(request,'restaurent_admin/subscription.html',{'standard':standard,'basic':basic,'premium':premium})
            else:
                return redirect('user-dashboard')

        else:
            return redirect('user-login')

    def post(self,request):
        data=CustomUser.objects.get(id=request.user.id)
        subscription_date=date.today()
        payment=request.POST.get('payment')
        package=request.POST.get('package')
        if package == 'Basic':
            subscritpion_expire_date=subscription_date+timedelta(days=30)
        elif package == 'Standerd':
            subscritpion_expire_date=subscription_date+timedelta(days=180)
        else:
            subscritpion_expire_date=subscription_date+timedelta(days=360)
        data.package=package
        data.subscritpion_expire_date=subscritpion_expire_date
        data.payment_price=payment
        data.subscription_date=subscription_date
        data.save()
        return redirect('Payment')

class Payment(View):
    def get(self,request):
        if request.user.is_authenticated:
            if CustomUser.objects.filter(payment_status='pending',id=request.user.id).exists():
                data=CustomUser.objects.get(id=request.user.id)
                return render(request,'restaurent_admin/payment.html',{'data':data})
            else:
                return redirect('user-dashboard')
        else:
            return redirect('user-login')
        
    def post(self,request):
        # print('sdbfjhsdbfsdffaffsdbasdafjasd')
        id=request.POST['id']
        data=CustomUser.objects.get(id=id)
        data.payment_status='Successfull'
        data.save()
        return redirect('user-dashboard')

class Receive_Notification(View):
    def get(self,request):
        if request.user.is_authenticated:
            data1=CustomUser.objects.get(id=request.user.id)
            time=date.today()
            newt=str(time)
            if newt > data1.subscritpion_expire_date:
                data1.payment_status='pending'
                data1.save()
                return redirect('subscription')
            else:
                data=Notification.objects.filter(receiver=request.user)
                context=[]
                for data in data:
                    d={
                        "heading":data.heading,
                        "description":data.description,
                        "id":data.id
                    }
                    context.append(d)
                    status=Notification.objects.get(id=data.id)
                    status.read=True
                    status.save()
                return render(request,'restaurent_admin/notification.html',{'data':context,'rname':data1})
        else:
            return redirect('user-login')

def delete_notification(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            data=Notification.objects.get(id=id)
            data.delete()
        return redirect('receive-notification')
    else:
            return redirect('user-login')

def generate_pdf(request):
    # Create a new PDF object
    data=CustomUser.objects.get(id=request.user.id)
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
    

class TermandConditions(View):
    def get(self,request):
        data=Termandcondition.objects.all()
        return render(request,'restaurent_admin/termandcondition.html',{'data':data})
class Privacyandpolicies(View):
    def get(self,request):
        data=PrivacyAndPolicy.objects.all()
        return render(request,'restaurent_admin/privcayandpolicy.html',{'data':data})

class Show_cat_image(View):
    def get(self,request):
        id=request.GET['id']
        img=CategoryImages.objects.get(id=id)
        imag=img.id
        src="/media/"+str(img.image)

        data={'cat_image':src,'image':imag}
        return JsonResponse(data) 

################Mobile View############
class Mobile_home(View):
    def get(self,request,id):
        user=CustomUser.objects.get(id=id)
        data=FoodCategories.objects.filter(user_id=user)
        return render(request,'mobile_view/home_page.html',{'data':data})
class Mobile_items(View):
    def get(self,request,id):
        data=FoodName.objects.filter(category_name=FoodCategories.objects.get(id=id))
        return render(request,'mobile_view/food_items.html',{'data':data})
class Addtocarts(View):
    def post(self,request,id):
        data=FoodName.objects.get(id=id)
        Addtocart.objects.create(user_id=data.user_id,food_id=data)
        return redirect('addtocardview',data.user_id.id)
class AddToCartView(View):
    def get(self,request,id):
        data=Addtocart.objects.filter(user_id=CustomUser.objects.get(id=id))
        return render(request,'mobile_view/addtocart.html',{'data':data})