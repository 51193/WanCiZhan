# usr/bin/env python
# -*- coding:utf-8- -*-
from django import forms
from users.models import User, Admin


class UserLoginForm(forms.Form):
    uid = forms.CharField(label='账号', max_length=20)
    password = forms.CharField(label='密码', max_length=20, widget=forms.PasswordInput)


class AdminLoginForm(forms.Form):
    uid = forms.CharField(label='账号', max_length=20)
    password = forms.CharField(label='密码', max_length=20, widget=forms.PasswordInput)
