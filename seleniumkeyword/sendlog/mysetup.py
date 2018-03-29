# -*- coding: utf-8 -*-
# mysetup.py 

from distutils.core import setup 
import py2exe 


"""
Py2exe打包程序
执行：python mysetup.py py2exe 
"""


setup(console=["syslogc.py"]) 


