
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser




class MyAccountManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError('Please Enter Email')
        if not password:
            raise ValueError('Please Enter Password')
        user=self.model(
            email  =  self.normalize_email(email),

        )
        user.is_active=True
        user.is_staff=False
        user.is_superuser=False
        user.set_password(password)
        user.save(using=self._db)
        return user
    


    def create_superuser(self,email,password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password
        )
       
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username        =models.CharField(max_length=50)
    email           =models.EmailField(max_length=100,unique=True)   
    password        =models.CharField(max_length=20,blank=False,null=False)
    is_staff        =models.BooleanField(default=False)
    is_active       =models.BooleanField(default=True)
    is_superuser    =models.BooleanField(default=False)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['password']
    
    objects=MyAccountManager()

    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_superuser
    def has_module_perms(self,add_label):
        return True


