from setuptools import setup, find_packages

setup(
    name='ImageComparator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'WatchUI',
        'openpyxl'
    ],
    author='Sonam Bindal',
    author_email='youremail@example.com',
    description='Custom library to help in Visual testing by comparing two images, and finding the difference',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shailucareer/ImageComparator.git',
    classifiers=[
        'Programming Language :: Python :: 3.12.1',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='=3.12.1',
)