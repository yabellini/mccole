import setuptools

setuptools.setup(
    name="mccole",
    version="0.1.0",
    url="https://github.com/gvwilson/mccole",
    author="Greg Wilson",
    author_email="gvwilson@third-bit.com",
    description="A simple publishing system",
    long_description=open("README.md").read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
