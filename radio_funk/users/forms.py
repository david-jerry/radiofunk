from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """
    name = forms.CharField(max_length=255, label='Name', widget=forms.TextInput(attrs={'title': 'Your Name', 'placeholder':'Firstname Lastname', "class":"textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 focus:z-10 sm:text-xl"}))
    # username = forms.CharField(max_length=255, label='Username', widget=forms.TextInput(attrs={'title': 'Your Username', 'placeholder':'Username', "class":"textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 focus:z-10 sm:text-xl"}))
    # email = forms.EmailField(max_length=255, label='Email', widget=forms.TextInput(attrs={'title': 'Your Email', 'placeholder':'Email', "class":"textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 focus:z-10 sm:text-xl"}))
    # password1 = forms.CharField(max_length=255, label='Password', widget=forms.TextInput(attrs={'title': 'Your Password', 'type':'password', 'placeholder':'Password', "class":"textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 focus:z-10 sm:text-xl"}))
    # password2 = forms.CharField(max_length=255, label='Confirm Password', widget=forms.TextInput(attrs={'title': 'Confirm Password', 'type':'password', 'placeholder':'Confirm Password', "class":"textinput textInput form-control appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 focus:z-10 sm:text-xl"}))

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.save()
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
