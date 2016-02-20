"""
Generate a haproxy config file based on etcd then gracefully reload haproxy
"""
from setuptools import find_packages, setup

dependencies = ['click>=6.2', 'mako>=1.0.1', 'urllib3>=1.14', 'apiclient>=1.0.2']

setup(
    name='haproxy-etcd',
    version='1.0.0',
    url='https://github.com/aksalj/haproxy-etcd',
    license='MIT',
    author='Salama AB',
    author_email='aksalj@aksalj.com',
    description='Generate a haproxy config file based on etcd then gracefully reload haproxy',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'haproxy-etcd = lib.__main__:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        # 'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
