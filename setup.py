from setuptools import setup, find_packages

setup(
    name='GRCMI',           
    version='0.1.0',               
    description='Short description of your package',
    author='Brandon Hearley',
    author_email='brandon.l.hearley@nasa.gov',
    url='https://github.com/bhearley/GRC_GrantaMI',
    packages=find_packages(),         
    install_requires=[
         'requests'
    ],              
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',          
)
