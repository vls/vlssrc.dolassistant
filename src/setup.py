# -*- coding: utf-8 -*-

from distutils.core import setup
from glob import glob
import py2exe

#python 2.6需要ms vc2008 crt runtime
#版本号为9.0.21022.8
#需要文件有manifests, msvcr90.dll, msvcp90.dll
#这些文件在python26安装目录 或 c:\windows\winsxs里
data_files = [("Microsoft.VC90.CRT", glob(r'e:\py\py26-ms-vc-runtime\*.*'))]
options = {
           "py2exe" : {'includes':['sip','PyQt4','google.protobuf','pkg_resources'],
                       'excludes':['_ssl'],
                       'dll_excludes': [
                            'MSVCP90.dll', "mswsock.dll", "powrprof.dll"
                            ],
                        'optimize' : 2,
                        'compressed' : True,
                        'bundle_files' : 1,
                          
                       }
           
           }

setup(
      data_files = data_files,
      options = options,
      windows = [{"script": "main.py"}],
      zipfile = None,
)