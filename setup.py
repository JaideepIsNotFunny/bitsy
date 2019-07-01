import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitsy",
    version="0.0.1",
    author="Jaideep Sagar",
    author_email="jaideep.mcs17.du@gmail.com",
    description="A Python tool to access 1D data bit wise.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JaideepSagar1997/bitsy",
    install_requires=[     
        'numpy',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)



