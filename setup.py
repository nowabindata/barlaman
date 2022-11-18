import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="barlaman",
    version="0.1.3",
    author="ANDAM Amine",
    author_email="andamamine83@gmail.com",
    description='Scrape data of Moroccan House of Representatives.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nowabindata/barlaman',
    keywords=["politics","parliament","webscraping","parliamentary-data","morocco"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
