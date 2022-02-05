from setuptools import find_packages, setup

from os import path
top_level_directory = path.abspath(path.dirname(__file__))
with open(path.join(top_level_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='netbox_ipmi_ovh',
    version='1.0.2',
    url='https://github.com/sanecz/netbox-ipmi-ovh',
    download_url='https://github.com/sanecz/netbox-ipmi-ovh/archive/v1.0.2.tar.gz',
    description='A tool to launch ipmi for ovh servers without going through the manager',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Lisa Bekdache',
    author_email='lisa.bekdache@gmail.com',
    install_requires=[
        'ovh'
    ],
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    keywords=['netbox', 'netbox-plugin', 'plugin'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
