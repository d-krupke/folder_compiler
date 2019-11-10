import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="folder_compiler",
    version="0.1.1",
    author="Dominik Krupke",
    author_email="krupked@gmail.com",
    description="A simple util for 'compiling' a folder, e.g. to a static website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d-krupke/folder_compiler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)