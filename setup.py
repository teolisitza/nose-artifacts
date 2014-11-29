#!/usr/bin/env python

from setuptools import setup, find_packages

tests_require = [
]

setup(
    name='nose-artifacts',
    version='0.1.1',
    author='Teo Lisitza',
    author_email='teo@cumulusnetworks.com',
    description='Give tests a place for artifacts',
    url='http://github.com/teolisitza/nose-artifacts',
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    install_requires=[
        'nose>=0.9',
    ],
    entry_points={
       'nose.plugins.0.10': [
            'nose_artifacts = nose_artifacts.plugin:ArtifactsPlugin'
        ]
    },
    license='Apache License 2.0',
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
