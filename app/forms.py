from django import forms
from .models import User,UserProfile
from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo']



class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone_number']
        
from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['account_number', 'total_amount', 'journal_number', 'screenshot', 'email', 'phone_number']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'readonly': 'readonly'}),
        }










