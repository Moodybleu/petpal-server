
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from .models import Appointments, Daily, Pet_Diary, User, Health, Pet


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(unique=True, max_length =250)
    email = forms.EmailField(db_index=True, unique=True, max_length = 250)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password' )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'password')
    list_filter = ('is_admin')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Pet)
admin.site.register(Pet_Diary)
admin.site.register(Health)
admin.site.register(Daily)
admin.site.register(Appointments)

class User(admin.ModelAdmin):
    list_display = ('id','username', 'email','password')

class Pet (admin.ModelAdmin):
    list_display = ('id', 'name', 'breed', 'date_of_birth', 'nickname', 'catchphrase','user')

class Health(admin.ModelAdmin):
    list_display = ("id","visit_date", "visit_type", "pet_weight","shots", "medicine", "other","tx_plan","pet")

class Daily(admin.ModelAdmin):
    list_display = ("id","food_schedule", "walk_schedule", "potty_trips", "medicine_schedule", "pet")

class Appointments(admin.ModelAdmin):
    list_display = ("id", "grooming", "play_date", "cuddles", "pet")
