from setuptools import setup
from os import path


PACKAGE_NAME = 'nameko_worker_logger'

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=PACKAGE_NAME,
    version='1.0.0',
    description='A package with logger for nameko worker',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/emlid/Nameko-logging-ELK',
    author='Emlid ltd.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=[PACKAGE_NAME],
    install_requires=[
        'nameko==2.11.0'
    ],
)
