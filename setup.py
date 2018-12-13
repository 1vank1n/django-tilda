from setuptools import setup


setup(
    name='django-tilda',
    version='1.0.9',
    author='Ivan Lukyanets',
    author_email='lukyanets.ivan@gmail.com',
    url='https://github.com/1vank1n/django-tilda',
    packages=[
        'tilda',
        'tilda.locale',
    ],
    include_package_data=True,
    license='MIT',
    description='A Django app for fetch/download pages from API Tilda.cc',
    keywords='django tilda',
    long_description=open('README.rst').read(),
    install_requires=[
        'django-object-actions==0.10.0',
        'requests==2.21.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
    ],
)
