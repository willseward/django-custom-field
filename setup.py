from setuptools import setup, find_packages

setup(
    name = "django-custom-field",
    version = "1.0",
    author = "David Burke",
    author_email = "david@burkesoftware.com",
    description = ("End user custom fields for Django including contrib.admin support"),
    license = "BSD",
    keywords = "django admin",
    url = "http://code.google.com/p/django-custom-field/",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: BSD License",
    ],
)
