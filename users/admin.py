# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Here you have to import the User model from your app!
from users.models.user import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    model = User
    list_display = ('id',
                    'email')
    search_fields = ('email',)
    ordering = ('id',)
    filter_horizontal = ()
