"""A setup module for patternlib."""


from setuptools import find_packages, setup


LONG_DESCRIPTION = """
An application that tracks your projects and tasks using sqlite3.
"""


setup(
    name='sqlite_api',
    version="0.0.1",
    description='API using Flask framework and sqlite3 database',
    long_description=LONG_DESCRIPTION,
    license = "BSD",
    url='https://github.com/gautamkhanapuri/tasks_api/commit/1b3837caf86fb0572f88da56949fcf90ed203672',
    author='gautamajey@gmail.com',
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Module',
        "License :: OSI Approved :: BSD License",
    ],
    packages=find_packages(where="code", exclude=[]),
    package_dir={'': 'code'},
    setup_requires=[],
    install_requires=[],
    python_requires='>=3.0',
)