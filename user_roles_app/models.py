from django.db import models

# Create your models here.
# user_roles_app/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)

class UserPermission(models.Model):
    admin = models.ForeignKey(User, related_name='admin_permissions', on_delete=models.CASCADE)
    normal_user = models.ForeignKey(User, related_name='normal_user_permissions', on_delete=models.CASCADE)
    permission_granted = models.BooleanField(default=False)
