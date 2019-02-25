#-*-coding:utf-8 -*-
import urllib
import os
import re
from devsapp import constant
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

def directory_file(document_root, ignore, root, dirs, original=None):
    """
    Take the results of an os.walk and apply the ignore and original
    file filters, works for both files and directories.
    """
        
    choices = []

    for d in dirs:
        if d in ignore: 
            continue
    
        d = os.path.join(root, d)
    
        if not original or not d.startswith(original): 
            d_short = d.replace(document_root, "", 1) 

            skip = 0

            if d_short in ignore: 
                skip = 1
            else:
                d_built = None
                for a in d_short.split('/'):
                    if d_built:
                        d_built = "%s/%s" % (d_built, a)
                    elif not a:
                        d_built = None
                    else: 
                        d_built = "/%s" % a

                    if d_built and d_built in ignore:
                        skip = 1 
   
            if not skip:
                choices.append((d, d_short))

    return choices

def get_ignore_list():
    "List of files to ignore."
    
    if not settings.FILE_IGNORE_LIST:
        return ''
    else:
        return settings.FILE_IGNORE_LIST

def get_max_upload_size():
    "Pull the FILE_UPLOAD_MAX_SIZE from settings."

    if not settings.FILE_UPLOAD_MAX_SIZE:
        raise ImproperlyConfigured, 'file_manager requires FILE_UPLOAD_MAX_SIZE variable be defined in settings.py'
    return settings.FILE_UPLOAD_MAX_SIZE

def get_document_root():
    """
    Pull the DOCUMENT_ROOT variable from settings. This variable is
    specific to this application.
    """
    if not settings.DOCUMENT_ROOT:
        raise ImproperlyConfigured, 'file_manager requires DOCUMENT_ROOT variable be defined in settings.py'
    return settings.DOCUMENT_ROOT

def clean_path(url):
    """
    Makes the path safe from '.', '..', and multiple slashes. Ensure all
    slashes point the right direction '/'.
    """
    if not url:
        return '' 

    result = ''
    path = os.path.normpath(urllib.unquote(url))
    path = path.lstrip('/')
    for part in path.split('/'):
        if not part:
            # Strip empty path components.
            continue
        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # Strip '.' and '..' in path.
            continue
        result = os.path.join(result, part).replace('\\', '/')
        
    if result and path != result or not path:
        result = ''
    
    return result

# Copied from python 2.6 
def commonprefix(m):
    "Given a list of pathnames, returns the longest common leading component"

    if not m: return ''
    s1 = min(m)
    s2 = max(m)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1

# Copied from python 2.6 
def relpath(path, start=os.path.curdir):
    "Return a relative version of a path"

    if not path:
        raise ValueError("no path specified")

    start_list = os.path.abspath(start).split(os.path.sep)
    path_list = os.path.abspath(path).split(os.path.sep)
           
    # Work out how much of the filepath is shared by start and path.
    i = len(commonprefix([start_list, path_list]))
           
    rel_list = [os.pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return curdir
    return os.path.join(*rel_list)

# From: django.contrib.admin.options
def log_addition(request, object):
    """
    Log that an object has been successfully added.

    The default implementation creates an admin LogEntry object.
    """
    from django.contrib.admin.models import LogEntry, ADDITION
    LogEntry.objects.log_action(
        user_id         = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id       = object.pk,
        object_repr     = force_unicode(object),
        action_flag     = ADDITION
    )

# From: django.contrib.admin.options
def log_change(request, object, message):
    """
    Log that an object has been successfully changed.

    The default implementation creates an admin LogEntry object.
    """
    from django.contrib.admin.models import LogEntry, CHANGE
    LogEntry.objects.log_action(
        user_id         = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id       = object.pk,
        object_repr     = force_unicode(object),
        action_flag     = CHANGE,
        change_message  = message
    )

# From: django.contrib.admin.options
def log_deletion(request, object, object_repr):
    """
    Log that an object has been successfully deleted. Note that since the
    object is deleted, it might no longer be safe to call *any* methods
    on the object, hence this method getting object_repr.

    The default implementation creates an admin LogEntry object.
    """
    from django.contrib.admin.models import LogEntry, DELETION
    from file_manager import models
    LogEntry.objects.log_action(
        user_id         = request.user.id,
        content_type_id = ContentType.objects.get_for_model(models.File).pk,
        object_id       = object.pk,
        object_repr     = object_repr,
        action_flag     = DELETION
    )



def  bash_writer(*args,**kwargs):
    return bash_head(*args,**kwargs)

def bash_head(author,time,*args,**kwargs):#author time
    string = "#!/bin/bash" + "\n"
    string = string + "# Author "+ author + "\n"

    string += "# Time " + time + "\n"

    return string + args_maker(*args,**kwargs)

def args_maker( *args, **kwargs):
    string = ""
    for key in kwargs:
        string += key + '=' + kwargs[key] +'\n'
    return string

def html2bash(str):#去除HTML p选项
    result , number = re.subn(constant.PATTERN_BR,'\n',str)
    result , number = re.subn(constant.PATTERN_P,'\n',result)
    result , number = re.subn(constant.PATTERN_F_P, '\n', result)
    return result

if __name__ == "__main__":
    kwargs={}
    print(bash_writer(author='Yo',time='2017-8-11 16:44:13',**kwargs))
    string = "<p>hostname<br>cat /proc/cpuinfo |grep processor|wc -l<br>free -m|sed -n '2p' |awk '{ print $2 }'<br>df -h |grep '/$' |awk '{ print $2 }'</p>"
    print(html2bash(string))