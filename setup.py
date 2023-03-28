import errno
import io
import os
import shutil
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand

__version__ = '2.0.0'
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
        user_home = os.path.expanduser("~")
        edam_home = os.path.join(user_home, ".edam")
        edam_templates = os.path.join(edam_home, "templates")
        edam_metadata = os.path.join(edam_home, "metadata")
        edam_inputs = os.path.join(edam_home, "inputs")
        edam_viewer = os.path.join(edam_home, ".viewer")
        directories = [edam_home, edam_templates, edam_metadata,
                       edam_inputs, edam_viewer]
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        resources = os.path.join(here, 'edam', 'resources')
        resource_dirs = ['inputs', 'templates', 'metadata']

        for directory in resource_dirs:
            copytree(os.path.join(resources, directory),
                     os.path.join(edam_home, directory))

        # Copy resource files
        shutil.copyfile(os.path.join(resources, 'settings.yaml'),
                        os.path.join(edam_home, 'settings.yaml'))

        shutil.copyfile(os.path.join(resources, 'edam.owl'),
                        os.path.join(edam_home, 'edam.owl'))

        shutil.copyfile(os.path.join(resources, 'edam.owl'),
                        os.path.join(edam_home, 'backup.owl'))

        # Copy flask_related contents into edam_home
        copytree(os.path.join(resources, 'flask_related'),
                 os.path.join(edam_home, '.viewer/'))

        shutil.rmtree(os.path.join(edam_home, '.viewer/', 'templates', 'edam'),
                      ignore_errors=True)
        # Create symlink templates into flask edam/templates
        os.symlink(os.path.join(edam_home, 'templates'),
                   os.path.join(edam_home, '.viewer', 'templates', 'edam'))


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


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='edam',
    version=__version__,
    url='https://github.com/BigDataWUR/EDAM',
    description='An input template framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GNU General Public License v3.0',
    author='Argyrios Samourkasidis',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=required,
    cmdclass={'test': PyTest, 'install': CustomInstall},
    python_requires='>=3.8',
    packages=find_packages(exclude=["tests.*", "tests"]),
    author_email='argysamo@gmail.com',
    package_data={
        'edam': ['resources/metadata/*', 'resources/inputs/*',
                 'resources/templates/*',
                 'resources/settings.yaml',
                 'resources/flask_related/static/*/*',
                 'resources/flask_related/templates/*/*', ],
    },
    entry_points={
        'console_scripts':
            ['edam=bin.read:cli', 'viewer=bin.viewer:run'],

    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

)
