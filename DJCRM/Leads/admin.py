from django.contrib import admin

# Register your models here.
from .models import Lead, User, Agent,UserProfile , Category


admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Agent)
