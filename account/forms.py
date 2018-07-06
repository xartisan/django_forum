from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        max_length=26,
        widget=forms.TextInput(
            attrs={
                "type": "username",
                "class": "form-control",
                "placeholder": "用户名",
                "autofocus": "",
            }),
        error_messages={
            "required": "用户名不能为空",
            "max_length": "用户名过长",
        })
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            "type": "password",
            "class": "form-control",
            "placeholder": "密码",
        }),
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码长度需大于8"
        })
    remember_me = forms.CharField(
        widget=forms.CheckboxInput(attrs={
            "type": "checkbox",
        }))


def repeat_validate():
    pass


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
        min_length=6,
        help_text='密码至少六位')
    password2 = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
        min_length=6,
        help_text='密码至少六位')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise ValidationError('两次密码输入不一致')
        return self.cleaned_data['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is not None and User.objects.filter(email=email).exists():
            raise ValidationError('该邮箱已经被注册')
        return email
