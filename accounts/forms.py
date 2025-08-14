from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
from .models import CustomUser


class CustomSignupForm(AllauthSignupForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['email2'] = forms.EmailField(
            label="Email (again)",
            widget=forms.TextInput(attrs={'autocomplete': 'email'})
        )
        self.fields['password2'].label = "Password (again)"
        self.fields.move_to_end('email2', last=False)
        self.fields.move_to_end('email', last=False)

    def save(self, request):
        user = super(AllauthSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'subscribed_to_news']