import errno
import io
import os
import shutil
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand

import edam

here = os.path.abspath(os.path.dirname(__file__))


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):

            try:
                shutil.copytree(s, d, symlinks, ignore)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        else:
            shutil.copy2(s, d)


# https://stackoverflow.com/questions/15853058/run-custom-task-when-call-pip-install
class CustomInstall(install):
    def run(self):
        install.run(self)
        # custom stuff here
        # create folders to put staff in.
        directories_to_be_created = [os.path.expanduser("~/.edam/"), os.path.expanduser("~/.edam/templates/"),
                                     os.path.expanduser("~/.edam/metadata/"),
                                     os.path.expanduser("~/.edam/inputs/"),
                                     os.path.expanduser("~/.edam/.viewer/")
                                     ]
        for directory in directories_to_be_created:
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        resources_directory = os.path.join(here, 'edam', 'resources')
        home_user_directory = os.path.expanduser("~/.edam/")
        directories_to_be_copied_from_resources = ['inputs', 'templates', 'metadata']

        for directory in directories_to_be_copied_from_resources:
            copytree(os.path.join(resources_directory, directory), os.path.join(home_user_directory, directory))
        shutil.copyfile(os.path.join(resources_directory, 'settings.yaml'),
                        os.path.join(home_user_directory, 'settings.yaml'))

        shutil.copyfile(os.path.join(resources_directory, 'edam.owl'),
                        os.path.join(home_user_directory, 'edam.owl'))

        shutil.copyfile(os.path.join(resources_directory, 'edam.owl'),
                        os.path.join(home_user_directory, 'backup.owl'))
        # Copy flask_related contents into home_directory

        copytree(os.path.join(resources_directory, 'flask_related'),
                 os.path.join(home_user_directory, '.viewer/'))
        # Copy edam templates into flask edam/templates
        copytree(os.path.join(resources_directory, 'templates'),
                 os.path.join(home_user_directory, '.viewer', 'templates', 'edam'))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='edam',
    version=edam.__version__,
    url='http://github.com/ecologismico/edam',
    description='An input template framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GNU General Public License v3.0',
    author='Argyrios Samourkasidis',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=['sqlalchemy', 'requests', 'numpy', 'pandas', 'numexpr', 'geopy', 'Flask-SQLAlchemy',
                      'Flask', 'Flask-Caching', 'jinja2', 'pyyaml', 'records', 'psycopg2', 'click',
                      'Flask-GoogleMaps==0.2.4', 'owlready2', 'pint', 'oyaml', 'Werkzeug'
                      ],
    cmdclass={'test': PyTest, 'install': CustomInstall},
    python_requires='>=3.3',
    packages=find_packages(exclude=["tests.*", "tests"]),
    author_email='argysamo@gmail.com',
    package_data={
        'edam': ['resources/metadata/*', 'resources/inputs/*', 'resources/templates/*',
                 'resources/settings.yaml', 'resources/flask_related/static/*/*',
                 'resources/flask_related/templates/*/*', ],
    },
    entry_points={
        'console_scripts':
            ['edam=bin.read:cli', 'viewer=bin.viewer:run'],

    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

)
