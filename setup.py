from setuptools import find_packages, setup


setup(
    name='django-tilda',
    version='1.1.0',
    author='Ivan Lukyanets',
    author_email='lukyanets.ivan@gmail.com',
    url='https://github.com/1vank1n/django-tilda',
    packages=find_packages(exclude=("example_project",)),
    include_package_data=True,
    license='MIT',
    description='A Django app for fetch/download pages from API Tilda.cc',
    keywords='django tilda',
    long_description=open('README.rst').read(),
    install_requires=[
        'django-object-actions>=0.10.0',
        'requests>=2.32.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
