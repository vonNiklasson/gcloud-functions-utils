from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = []
for package in setuptools.find_packages():
    if not package.startswith('tests'):
        packages.append(package)

setup(
    name='google-pubsub-utils',
    version='0.3.0',
    author="Johan Niklasson",
    author_email="johan@niklasson.me",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vonNiklasson/google-pubsub-utils",
    packages=packages,
    install_requires=[
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
