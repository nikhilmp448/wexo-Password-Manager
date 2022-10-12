from django.contrib import admin

from .models import Password,OrgMember, OrgPassword, Organisation

# Register your models here.
admin.site.register(Password)
admin.site.register(Organisation)
admin.site.register(OrgMember)
admin.site.register(OrgPassword)