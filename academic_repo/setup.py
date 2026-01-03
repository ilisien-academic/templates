from setuptools import setup, find_packages

setup(
    name='academic-repo-tool',
    version='1.0.0',
    packages=find_packages(),
    package_data={
        'academic_repo': [
            'templates/**/*',
            '*.json',
        ],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'academic-repo=academic_repo.main:main',
        ],
    },
)
