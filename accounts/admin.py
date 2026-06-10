from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fitness_goal', 'membership_status')

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
