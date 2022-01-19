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
    install_requires=["markdown-it-py>=2.0.0", "mdit-py-plugins>=0.3.0"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
