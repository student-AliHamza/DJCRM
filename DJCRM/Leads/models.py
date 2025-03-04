from django.db import models
# its used for authentication that django works itself
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save

# Create your models here.
# class User(AbstractUser):
#     pass
# Now make custum user Abstract models
class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Lead(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organisation = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    agent = models.ForeignKey('Agent', null=True, blank=True,on_delete=models.SET_NULL)
    Category = models.ForeignKey('Category',related_name="leads", null=True, blank=True,on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
  
class Agent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email
   
class Category(models.Model):   # New , Contacted , Converted , Unconverted
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile ,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
   


#    its used for every email is attached to the login
def post_user_created_signals(sender,instance,created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(post_user_created_signals,sender=User)
 

