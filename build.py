from setuptools import setup, find_packages

setup(
    name='resume-cli',
    version='0.1.3',
    packages=(
    find_packages(include=['resuMe','resuMe/*'])+
    find_packages()
    ),
    include_package_data=True,
    install_requires=[
        'click==7.1.2',
        'PyInquirer==1.0.3',
        'selenium== 3.141.0',
        'bs4==0.0.1',
        'requests==2.26.0',
        'lxml==4.6.3',
        'webdriver-manager==3.4.1',
        'colorama==0.4.4',
        'psutil==5.8.0'
    ],
    entry_points={
        'console_scripts': [
            'resume-cli = resuMe.main:init',
        ],
    },
)