from email.policy import default
from django.db import models
# Create your models here.
from user.models import Account
from password import encryption_util


class Password(models.Model):
    user = models.ForeignKey(Account,related_name='pass_owner',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Organisation(models.Model):
    user = models.ForeignKey(Account,related_name='org_owner',on_delete=models.CASCADE)
    org_name = models.CharField(max_length=100)

    def __str__(self):
        return self.org_name


class OrgMember(models.Model):
    members = models.ForeignKey(Account,related_name='members',on_delete=models.CASCADE,null=True,blank=True)
    organisation = models.ForeignKey(Organisation,related_name='OrgMember',on_delete=models.CASCADE)
    def __str__(self):
        return self.organisation.org_name

class OrgPassword(models.Model):
    organisation = models.ForeignKey(Organisation,related_name='OrgPassword',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=3000)

    def __str__(self):
        return self.organisation.org_name


class HassPermission(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='user')
    share_to = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='share_to')
    pass_id = models.ForeignKey(OrgPassword,on_delete=models.CASCADE)