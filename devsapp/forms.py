# -*-coding:utf-8 -*-
from django import forms
from .models import *
from django.contrib.auth.models import User

class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        exclude = ['node_singer']
class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        exclude = ['line_signer']

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ['device_signer']
class HostfForm(forms.ModelForm):
    class Meta:
        model = SSHInfo
        exclude = ['state']
class AssetForm(forms.ModelForm):
    class Meta:
        model = Assets
        exclude = ['status']
class PlayHost(forms.Form):
    commands=[
        ('df -h','df -h'),
        ('ifconfig','ifconfig'),
        ('free -m','free -m'),
    ]
    ips = forms.ModelChoiceField(label='hosts',queryset=SSHInfo.objects.all())
    user = forms.CharField()
    pwd = forms.CharField(widget=forms.PasswordInput())
    comm = forms.ChoiceField(required=True,choices=commands)

class AnsibleForm(forms.Form):
    type = [('shell','shell'),('command','command'),('script','script')]
    # ips = forms.CharField()
    ips = forms.ModelMultipleChoiceField(queryset=Assets.objects.all())
    modules = forms.ChoiceField(required=True,choices=type)
    arg = forms.CharField()



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","password","email"]

class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"原密码",
                'rows': 1,
            }
        ),
    )
    newpassword1 = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"新密码",
                'rows': 1,
            }
        ),
    )
    newpassword2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
                'rows': 1,
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] <> self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data


class RegistForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')

