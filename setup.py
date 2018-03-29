# -*- coding:utf-8 -*-
__author__ = 'Ray'


import os
from setuptools import setup, find_packages, Command


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


def do_setup():
    setup(
        name='automagic',
        description='',
        license='GPL 2.0',
        version='0.1',
        packages=find_packages(exclude=['tests*']),
        include_package_data=True,
        zip_safe=False,
        scripts=[],
        install_requires=[
            'django>=1.11.1',
            'MySQL-Python>=1.2.3',
            'django-users2==0.2.1',
            'django-cors-headers==2.0.2',
            'djangorestframework==3.6.3',
            'python-jenkins==0.4.14',
            # seleniumKeyword Lib
            'selenium',
            'requests',
            'paramiko == 2.1.2',
            'scapy == 2.3.3',
        ],
        setup_requires=[
        ],
        extras_require={
        },
        classifiers=[
        ],
        author='Ray',
        author_email='tsbc@vip.qq.com',
        url='',
        download_url=(),
        cmdclass={
            'extra_clean': CleanCommand,
        },
    )

if __name__ == "__main__":
    do_setup()


