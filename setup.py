import os

import glob
import shutil
import gazeroct

from setuptools import setup, find_packages, Command


class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for folder in ['build', 'dist']:
            if os.path.exists(folder):
                shutil.rmtree(folder)
        for egg_file in glob.glob('*egg-info'):
            shutil.rmtree(egg_file)


setup(
    name='gazeroct',
    version=gazeroct.__version__,
    url='https://github.ibm.com/aur-mma/gazer-oct',
    license='IBM',
    author='Stefan Maetschke',
    author_email='stefanrm@au1.ibm.com',
    description='Annotation tool for OCT images',
    install_requires=[
        'Kivy >= 1.9.1',
        'pyyaml >= 3.12',
        'pandas >= 0.18.1',
    ],
    platforms='any',
    packages=find_packages(exclude=['setup']),
    include_package_data=True,
    cmdclass={
        'clean': CleanCommand,
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
