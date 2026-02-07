from setuptools import setup, find_packages

setup(
    name='CtrlRound',
    version='0.6.0',
    packages=find_packages(),
    install_requires=[
        numpy>=1.23.5
        pandas>=2.1.2
    ],
    author='Christian Gagné',
    author_email='christian.gagne@gmail.com',
    description='Performs controlled rounding of tabular data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/veozen/CtrlRound',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
