# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Here you have to import the User model from your app!
from users.models.user import User

#
# @admin.register(User)
# class MyUserAdmin(UserAdmin):
#     model = User
#     list_display = ('phone_number',
#                     'email')
#     list_filter = ('phone_number',
#                    'email')
#     search_fields = ('phone_number',)
#     ordering = ('phone_number',)
#     filter_horizontal = ()
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('phone_number',)}),
#     )
#     # I've added this 'add_fieldset'
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('phone_number', 'password1', 'password2'),
#         }),
#     )
