from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from .models import *

class UserAdmin(admin.ModelAdmin):
    model = User

# Register your models here.

admin.site.unregister(Group)

#Re-register Admin with new model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#Register book model to admin site
#admin.site.register(Book)
#admin.site.register(LoanInstance)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status',)
    list_filter = ('user',)


@admin.register(LoanInstance)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loaner', 'book_loaned', 'loan_status', 'due_date',)

admin.site.register(BulletinGroup)
admin.site.register(News)
admin.site.register(Library)
admin.site.register(Post)