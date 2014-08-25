
import navtrix

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='navtrix',
    version=navtrix.__version__,
    description="Navtrix tracks position and rotation in a Transform class",
    author="Eric Olson",
    author_email="me@olsoneric.com",
    maintainer="Eric Olson",
    maintainer_email="me@olsoneric.com",
    url="http://github.com/olsoneric/navtrix",
    packages=['navtrix'],
    package_data={'': ['LICENSE', 'NOTICE', 'README.md']},
    package_dir={'navtrix': 'navtrix'},
    include_package_data=True,
    license='Apache 2.0',
    keywords=["transform", "matrix", "quaternion"],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    long_description=readme,
)
