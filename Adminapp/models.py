from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class CustomuserManager(BaseUserManager):
    def create_user(self  , email_id , password , phone_number  ):
       
        if not email_id:
            raise ValueError("The Email must be set")
        user = self.model(
            email_id=self.normalize_email(email_id),
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self , full_name , email_id , password , phone_number , choose_profilepic ):
        """
        Creates and saves a superuser with the given email, name, tc and password.
        """
        user = self.create_user(
            full_name=full_name,
            email_id=email_id,
            phone_number=phone_number,
            choose_profilepic=choose_profilepic,
            password=password
        )
        
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractBaseUser):
    email_id = models.EmailField(verbose_name='email_id', max_length=255, unique=True, null=True)
    full_name=models.CharField(max_length=1000,null=True,blank=True)
    phone_number = models.CharField(max_length=10,null=True,blank=True)
    choose_profilepic = models.FileField(null=True,blank=True,upload_to='profile')
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    is_superuser = models.BooleanField(default=False)



    objects = CustomuserManager()

    USERNAME_FIELD = 'email_id'
    EMAIL_FIELD = 'email_id'
    REQUIRED_FIELDS = ['full_name','phone_number','choose_profilepic']

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
    receiver = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)\
    
class Termandcondition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True,blank=True)

class PrivacyAndPolicy(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True,blank=True)