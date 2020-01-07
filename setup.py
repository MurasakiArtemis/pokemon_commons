import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pokemon_commons',
    version='0.1',
    author="Murasaki Artemis",
    author_email="murasaki_artemis@outlook.com",
    description="A package containing pokemon SQLAlchemy classes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MurasakiArtemis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'SQLAlchemy==1.3.11',
        'SQLAlchemy-Utils==0.36.0',
    ],
)
