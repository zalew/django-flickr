import os
from setuptools import setup, find_packages
from flickr import VERSION, DEV_STATUS

setup(
    name='django-flickr',
    version='.'.join(map(str, VERSION)),
    description='Mirror your Flickr into Django.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    keywords='django flickr photo photography photoblog',
    author='Jakub Zalewski',
    author_email='zalew7@gmail.com',
    url='https://bitbucket.org/zalew/django-flickr',
    license='public domain',
    packages=find_packages(),
    zip_safe=False,
    package_data = {
        'flickr': [],
    },
    classifiers=[
        'Development Status :: %s' % DEV_STATUS,
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=[
        'django >= 1.2',
        'bunch >= 1.0',
        'django-taggit >= 0.9',
        'django-taggit-templatetags >= 0.4',
    ],    
)
