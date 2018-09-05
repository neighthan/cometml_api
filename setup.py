import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="cometml_api",
    version="0.1",
    author="Nathan Hunt",
    author_email="neighthan.hunt@gmail.com",
    description="Python bindings for the CometML REST API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neighthan/cometml_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
