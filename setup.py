from setuptools import setup, find_packages


def load_reqs(file_name):
    with open(file_name) as fd:
        return fd.readlines()

def load_version(file_name):
    with open(file_name) as fd:
        for line in fd:
            if '__version__' in line:
                version_string = line.split('=')[1]
                return version_string.replace('\'"', '')


setup(
    name='swap',
    version=load_version('swap/__init__.py'),
    description='Test assignment for backend developer',
    author_name='Rinat Sabitov',
    author_email='rinat.sabitov@gmail.com',
    packages=find_packages(exclude=['lib/']),
    install_requires=load_reqs('requirements.txt'),
    tests_require=load_reqs('test-requirements.txt')
)
