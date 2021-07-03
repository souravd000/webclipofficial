from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user




class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



class profileUpdateForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['image', 'Cover_Video', 'Bio', 'Birthday', 'Gender', 'Relationship_status', 'Location' , 'website', 'QR_Snap', 'UPI_id', 'Deactivate_Contributions']










