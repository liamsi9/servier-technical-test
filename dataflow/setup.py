import setuptools

setuptools.setup(
    name='SERVIER-TEST-PACKAGE',
    version='0.1',
    install_requires=["google-cloud-storage==1.44.0"],
    packages=setuptools.find_packages(),
)