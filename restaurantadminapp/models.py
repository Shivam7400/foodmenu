from django.db import models
from Adminapp.models import CustomUser
from django.core.files import File
from io import BytesIO
from PIL import Image, ImageDraw
# Create your models here.

    

class FoodCategories(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    category_image=models.ImageField(upload_to='category_image',null=True,blank=True)
    category_name=models.CharField(max_length=200,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class FoodName(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    category_name=models.ForeignKey(FoodCategories,on_delete=models.CASCADE, related_name="cat", null=True)
    food_name=models.CharField(max_length=200,null=True,blank=True)
    food_image=models.ImageField(upload_to='food_image',null=True,blank=True)
    price=models.FloatField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=100,null=True)

class AddOnes(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    price=models.FloatField(null=True,blank=True)
    foodname=models.ForeignKey(FoodName, on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Addtocart(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    food_id=models.ForeignKey(FoodName, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)