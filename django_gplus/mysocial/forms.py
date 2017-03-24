from django import forms

from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    user_exist = False
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User.objects.get(username=username)
            self.user_exist = True
        except User.DoesNotExist:
            raise forms.ValidationError("Are you sure you are registered? We cannot find this user.")
        return username

    def clean_password(self):
        if self.user_exist:
            username = self.cleaned_data.get("username")
            user = User.objects.get(username=username)
            password = self.cleaned_data.get("password")
            if user.check_password(password) and user.is_active:
                return password
            else:
                raise forms.ValidationError("Invalid Password or inactive user")

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Your Email')
    password1 = forms.CharField(label='Password', \
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password Confirmation', \
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError(
                    "This email has already been registered. Please check and try again or reset your password.")
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user