from django.db import models
from Adminapp.models import CustomUser
import qrcode
from django.core.files import File
from io import BytesIO
from PIL import Image, ImageDraw
# Create your models here.

class RestaurentDetails(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    restaurant_name=models.CharField(max_length=1000,null=True,blank=True)
    restaurant_id=models.CharField(max_length=300,null=True,blank=True,unique=True)
    restaurant_address=models.CharField(max_length=3000,null=True,blank=True)
    qr_code=models.ImageField(upload_to='qr_code',blank=True)
    payment_status=models.CharField(max_length=200,default='pending')
    payment_price=models.CharField(max_length=200,default='0')
    is_active = models.BooleanField(default = True)

    
    def save(self,*args,**kwargs):
        qrcode_image=qrcode.make('192.168.0.235:8000/menu'+'/'+self.restaurant_name)
        canvas=Image.new('RGB',(350,350),'white')
        draw=ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        fname=f'qu_code-{self.restaurant_name}'+'.png'
        buffer=BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname,File(buffer),save=False)
        canvas.close()
        super().save(*args,**kwargs)
        
    

class FoodCategories(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    restaurant_id=models.ForeignKey(RestaurentDetails,on_delete=models.CASCADE,null=True)
    category_name=models.CharField(max_length=200,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



class FoodName(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    category_name=models.ForeignKey(FoodCategories,on_delete=models.CASCADE, related_name="cat", null=True)
    food_name=models.CharField(max_length=200,null=True,blank=True)
    food_image=models.ImageField(upload_to='food_image',null=True,blank=True)
    full_price=models.CharField(max_length=200,null=True,blank=True,default='-')
    medium_price=models.CharField(max_length=200,null=True,blank=True,default='-')
    small_price=models.CharField(max_length=200,null=True,blank=True,default='-')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
