from setuptools import setup

setup(
    name='academic-repo-tool',
    version='1.0.0',
    py_modules=['templates'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'academic-repo=your_script_name:main',
        ],
    },
)