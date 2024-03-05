from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor_uploader.fields import RichTextUploadingField
import qrcode
from django.core.files import File
from io import BytesIO
from PIL import Image, ImageDraw

# Create your models here.
class CustomuserManager(BaseUserManager):
    def create_user(self  , email_id , password , phone_number,restaurant_name,restaurant_logo,restaurant_address  ):
       
        if not email_id:
            raise ValueError("The Email must be set")
        user = self.model(
            email_id=self.normalize_email(email_id),
            phone_number=phone_number,
            restaurant_name=restaurant_name,
            restaurant_logo=restaurant_logo,
            restaurant_address=restaurant_address,

        )
        user.set_password(password)
        user.save(using=self._db)
        print(user)
        return user
    

    def create_superuser(self , full_name , email_id , password , phone_number  ):
        """
        Creates and saves a superuser with the given email, name, tc and password.
        """
        user = self.create_user(
            full_name=full_name,
            email_id=email_id,
            phone_number=phone_number,
            password=password
        )
        
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractBaseUser):
    email_id = models.EmailField(verbose_name='email_id', max_length=255, unique=True, null=True)
    username=models.CharField(max_length=1000,null=True,blank=True)
    full_name=models.CharField(max_length=1000,null=True,blank=True)
    phone_number = models.CharField(max_length=10,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    is_superuser = models.BooleanField(default=False)
    restaurant_name=models.CharField(max_length=1000,null=True,blank=True)
    restaurant_logo=models.FileField(upload_to='restaurant_logo' ,blank=True)
    restaurant_address=models.CharField(max_length=3000,null=True,blank=True)
    qr_code=models.ImageField(upload_to='qr_code',blank=True)
    payment_status=models.CharField(max_length=200,default='pending')
    payment_price=models.CharField(max_length=200,default='0')
    package=models.CharField(max_length=200,default='pending')
    subscription_date=models.CharField(null=True,blank=True,max_length=100)
    subscritpion_expire_date=models.CharField(null=True,blank=True,max_length=100)
    
    def __str__(self):
        return f'{self.email} - {self.id}'

    def save(self,*args,**kwargs):
        url = f'http://69.49.235.253:8026/mobile-home/{self.id}'

        # Generate the QR code with version=None to determine the best version automatically
        qr_code_image = qrcode.make(url, version=None, error_correction=qrcode.constants.ERROR_CORRECT_H)

        # Calculate the new size to maintain equal sides and improve resolution
        new_size = max(qr_code_image.size) + 40

        # Create a new canvas with the calculated size
        canvas = Image.new('RGB', (new_size, new_size), 'white')
        draw = ImageDraw.Draw(canvas)

        # Paste the QR code image in the center of the canvas
        qr_code_position = ((new_size - qr_code_image.size[0]) // 2, (new_size - qr_code_image.size[1]) // 2)
        canvas.paste(qr_code_image, qr_code_position)

        fname = f'qu_code-{self.restaurant_name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


    objects = CustomuserManager()

    USERNAME_FIELD = 'email_id'
    EMAIL_FIELD = 'email_id'
    REQUIRED_FIELDS = ['full_name','phone_number',]

    def __str__(self):
        return self.email_id
    

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class SubscriptionDetails(models.Model):
    heading=models.CharField(max_length=200,null=True,blank=True)
    subscription_price=models.IntegerField(null=True,blank=True)
    subscription_duration=models.IntegerField(null=True,blank=True)

class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True,blank=True)
    heading = models.CharField(max_length=1000,null=True,blank=True)
    sender = models.CharField(max_length=1000,null=True,blank=True)
    receiver = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    read=models.BooleanField(default=False)
    


class Termandcondition(models.Model):
    img=models.ImageField(null=True,blank=True,upload_to='condition')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = RichTextUploadingField(max_length=100,null=True,blank=True)

class PrivacyAndPolicy(models.Model):
    img=models.ImageField(null=True,blank=True,upload_to='condition')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True,blank=True)
class CategoryImages(models.Model):
    image=models.ImageField(null=True,blank=True,upload_to='condition')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)