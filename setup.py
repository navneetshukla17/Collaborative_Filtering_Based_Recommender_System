from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

REPO_NAME = "Collaborative_Filtering_Based_Recommender_System"
AUTHOR_USER_NAME = "TUSHAR SHUKLA"
SRC_REPO = "Collaborative_Filtering_Based_Recommender_System"
LIST_OF_REQUIREMENTS = []

setup(
    name=SRC_REPO,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    description="A small package for Collaborative Filtering Based Recommender System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/navneetshukla17/Collaborative_Filtering_Based_Recommender_System",
    author_email="tusharshukla707@gmail.com",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)