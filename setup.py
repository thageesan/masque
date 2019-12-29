from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author='Thageesan Thanbalasingam',
    author_email='thageesan@gmail.com',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: No-License',
        'Programming Language :: Python :: 3.8',
    ],
    description='',
    install_requires=requirements,
    license='UNLICENSED',
    long_description=readme + '\n\n',
    include_package_data=True,
    keywords='',
    name='masque',
    packages=find_packages(include=['masque', 'masque.model']),
    setup_requires=setup_requirements,
    url='',
    version='0.1.0',
    zip_safe=False,
    entry_point={
        'console_scripts': [
            'masque=masque',
        ]
    }
)
