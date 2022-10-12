from organisation.views import Org_Members, Org_Password, OrganisationViewSet
from user.views import  UserListViewSet, UserRegisterViewSet
from rest_framework.routers import DefaultRouter

from password.views import MyPasswordViewSet, sharePassword, sharedPassword



router = DefaultRouter()
urlpatterns=[]


router.register(r'UserRegister',UserRegisterViewSet,basename='UserRegister')
router.register(r'mypassword',MyPasswordViewSet,basename='mypassword')
router.register(r'createOrganisation',OrganisationViewSet,basename='createOrganisation')
router.register(r'AddToOrganisation',Org_Members,basename='AddToOrganisation')
router.register(r'OrganisationPassword',Org_Password,basename='OrganisationPassword')
router.register(r'sharePassword',sharePassword,basename='sharePassword')
router.register(r'UserListViewSet',UserListViewSet,basename='UserListViewSet')
router.register(r'sharedPass',sharedPassword,basename='sharedPass')





urlpatterns=urlpatterns+router.urls