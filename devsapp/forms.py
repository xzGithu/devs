# -*-coding:utf-8 -*-
from django import forms
from .models import *
from django.contrib.auth.models import User
import os
from django.utils.translation import ugettext as _
from devsapp import utils



class query_form(forms.Form):
    hostip = forms.ModelChoiceField(label='hosts',queryset=Items.objects.values_list("hostid", flat=True).distinct())
    metric = forms.ModelChoiceField(label='metrics',queryset=Items.objects.values_list("itemid", flat=True).distinct())

class command_apiform(forms.Form):
    hostip=forms.CharField()
    command=forms.CharField()
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
        widgets = {
            'pwd':forms.PasswordInput(),
        }
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
    ips = forms.ModelChoiceField(label='hosts',queryset=Assets.objects.all())
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
        fields = ["username","is_active","is_superuser","user_permissions","email"]

class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                # 'placeholder': u"原密码",
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
                # 'placeholder': u"新密码",
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
                # 'placeholder': u"确认密码",
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
    repassword = forms.CharField(label='确认密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')



class ScriptCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Script
        # fields = ['name','script','author','info']
        fields = ['script','name','info']
        labels = {
            'script':'脚本内容','info':'脚本信息','name':'脚本名称',
        }
        widgets = {
            'script':forms.Textarea(attrs={'style':'height:500px;','class':'summernote'}),
        }

class ScriptArgsCreateUpdateForm(forms.ModelForm):
    class Meta:
            model = ScriptArgs
            fields = ['args_name', 'args_value']
            labels = {
                'args_name': '参数名称',
                'args_value': '参数默认数值'
            }
            widgets = {
                'args_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
                'args_value': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
            }


class DirectoryFileForm(forms.Form):
    link = forms.ChoiceField(help_text=_('Link Destination'))

    def __init__(self, file, *args, **kwargs):
        self.file = file
        self.document_root = utils.get_document_root()
        super(DirectoryFileForm, self).__init__(*args, **kwargs)

        # Set the choices dynamicly.
        self.fields['link'].choices = self.make_choices()

    def make_choices(self):

        choices = []
        ignore = utils.get_ignore_list()

        # Make "/" valid"
        d = self.document_root
        d_short = d.replace(self.document_root, "", 1)
        if not d_short:
            d_short = '/'

        choices.append((d, d_short))

        for root, dirs, files in os.walk(self.document_root):
            if root in ignore:
                continue

            choices.extend(utils.directory_file(self.document_root, ignore, root, dirs))
            choices.extend(utils.directory_file(self.document_root, ignore, root, files))

        # return sorted(choices)
        choices.sort()
        return choices

    def clean_parent(self):
        parent = self.cleaned_data['parent']

        path = os.path.join(parent, self.file)

        if self.original != path:  # Let no change work correctly.
            if os.access(path, os.F_OK):
                raise forms.ValidationError(_('Destination already exists.'))
            if path.startswith(self.original):
                raise forms.ValidationError(_('Can\'t move directory into itself.'))

        if not os.access(parent, os.W_OK):
            raise forms.ValidationError(_('Can not write to directory.'))

        return parent


class DirectoryForm(forms.Form):
    parent = forms.ChoiceField(help_text=_('Destination Directory'))

    def __init__(self, file, original, *args, **kwargs):
        self.file = file
        self.original = original
        self.document_root = utils.get_document_root()
        super(DirectoryForm, self).__init__(*args, **kwargs)

        # Set the choices dynamicly.
        self.fields['parent'].choices = self.make_choices()

    def make_choices(self):

        choices = []
        ignore = utils.get_ignore_list()

        # Make "/" valid"
        d = self.document_root
        d_short = d.replace(self.document_root, "", 1)
        if not d_short:
            d_short = '/'

        choices.append((d, d_short))

        for root, dirs, files in os.walk(self.document_root):
            choices.extend(utils.directory_file(self.document_root, ignore, root, dirs, self.original))

        # return sorted(choices)
        choices.sort()
        return choices

    def clean_parent(self):
        parent = self.cleaned_data['parent']

        path = os.path.join(parent, self.file)

        if self.original != path:  # Let no change work correctly.
            if os.access(path, os.F_OK):
                raise forms.ValidationError(_('Destination already exists.'))
            if path.startswith(self.original):
                raise forms.ValidationError(_('Can\'t move directory into itself.'))

        if not os.access(parent, os.W_OK):
            raise forms.ValidationError(_('Can not write to directory.'))

        return parent


class NameForm(forms.Form):
    name = forms.CharField()

    def __init__(self, path, original, *args, **kwargs):
        self.path = path
        self.original = original
        super(NameForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']

        path = os.path.join(self.path, name)

        if self.original != path:  # Let no change work correctly.
            if os.access(path, os.F_OK):
                raise forms.ValidationError(_('Name already exists.'))

        return name


class ContentForm(forms.Form):
    attrs = {'class': 'vLargeTextField'}
    content = forms.CharField(widget=forms.widgets.Textarea(attrs=attrs))


class CreateForm(NameForm, ContentForm):
    pass


class CopyForm(NameForm, DirectoryForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        name = self.cleaned_data.get('name')
        parent = self.cleaned_data.get('parent')

        path = os.path.join(parent, name)

        if os.access(path, os.F_OK):
            raise forms.ValidationError(_('File name already exists.'))

        return cleaned_data


class CreateLinkForm(NameForm, DirectoryFileForm):
    pass


class PermissionForm(forms.Form):
    pass


class UploadForm(forms.Form):
    file = forms.FileField()

    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(UploadForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        filename = self.cleaned_data['file'].name

        if os.access(os.path.join(self.path, filename), os.F_OK):
            raise forms.ValidationError(_('File already exists.'))

            # CHECK FILESIZE
        filesize = self.cleaned_data['file'].size
        if filesize > utils.get_max_upload_size():
            raise forms.ValidationError(_(u'Filesize exceeds allowed Upload Size.'))

        return self.cleaned_data['file']
