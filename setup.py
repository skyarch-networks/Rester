from setuptools import setup

setup(name='Rester',
    version='1.0.2.10',
    author='Shota Tsunehiro',
    author_email='tomoka319@gmail.com',
    url='https://github.com/skyarch-networks/rester',
    license='LICENSE.txt',
    packages=['rester'],
    entry_points={
        'console_scripts':['apirunner = rester.apirunner:run']
    },
    test_suite="test",
    description='Rest API Testing',
    long_description=open('README.md').read(),
    install_requires=["requests", "testfixtures", "PyYAML>=3.9", "boto3", "requests-aws4auth", "warrant"],
)
