from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class RegisterForm(forms.Form):
    user = forms.CharField(max_length=25, label='用户名', widget=forms.TextInput(attrs={
        'id': 'user_name'
    }))
    password = forms.CharField(widget=forms.PasswordInput(
        {'id': 'pwd'}
    ), label='密码')
    password_confirmation = forms.CharField(widget=forms.PasswordInput(
        {'id': 'cpwd'}
    ), label='确认密码')
    email = forms.EmailField(required=False, label='邮箱(可选)',widget=forms.EmailInput(
        {
            'id': 'email'
        }
    ))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        user = cleaned_data.get('user')
        password_confirmation = cleaned_data.get('password_confirmation')
        if password_confirmation != password:
            raise  ValidationError('两次密码不一致')
        if len(password) < 5 or len(password) > 20:
            raise ValidationError('密码长度在5-20之间')
        if User.objects.filter(username=user).exists():
            raise ValidationError('用户已存在')


class Login(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(Login, self).__init__(*args, **kwargs)
    user = forms.CharField(max_length=20, label='用户名',widget=forms.TextInput({
        'id': 'login_user', 'class': 'name_input', 'placeholder': '请输入用户名'
    }))
    password = forms.CharField(widget=forms.PasswordInput({
        'id': 'login_password', 'class': 'pass_input', 'placeholder': '请输入密码'
    }), label='密码')
    verifycode = forms.CharField(label='验证码', widget=forms.TextInput({
        'class': 'vc_input', 'placeholder': '请输入验证码'
    }))
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        user = cleaned_data.get('user')
        verifycode = cleaned_data.get('verifycode')
        session_verifycode = self.request.session.get('verifycode')
        if verifycode and session_verifycode:
            verifycode = verifycode.lower()
            session_verifycode = session_verifycode.lower()
            # if verifycode != session_verifycode:
            #     raise ValidationError('验证码错误')
        if not User.objects.filter(username = user).exists():
            raise ValidationError('用户不存在')
        if len(password) < 5 or len(password) > 20:
            raise ValidationError('密码长度在5-20之间')