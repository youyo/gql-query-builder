#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, Command, find_packages
from pip._internal.req import parse_requirements
import os

install_reqs = parse_requirements('requirements.txt', session='hack')
requires = [str(ir.req) for ir in install_reqs]


class PublishCommand(Command):
    user_options: list = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -rf dist/')
        os.system('python setup.py sdist')
        os.system('twine upload dist/*')


setup(
    name='gql-query-builder',
    description='This is a GraphQL query builder.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    use_scm_version=True,
    url='https://github.com/youyo/gql-query-builder',
    author='youyo',
    author_email='1003ni2@gmail.com',
    install_requires=requires,
    license="MIT License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='graphql gql query-builder',
    packages=['gql_query_builder'],
    python_requires='>=3.6',
    project_urls={
        'Source': 'https://github.com/youyo/gql-query-builder',
    },
    cmdclass={'publish': PublishCommand},
)
