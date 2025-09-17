import io
import os
import configparser
from setuptools import setup, find_packages

# --- Long description (robust UTF-8, fallback if README missing) ---
readme = ""
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with io.open(readme_path, "r", encoding="utf-8") as fh:
        readme = fh.read()
else:
    readme = "CSO Classifier: classify scientific documents with topics from the Computer Science Ontology."

# --- Requirements ---
requirements_to_install = [
    "gensim>=4.3.3",             # modern Gensim API, compatible with Python 3.12
    "spacy>=3.7.4",               # works with Pydantic v2
    "kneed>=0.8.5",
    "igraph>=0.11.4",
    "hurry.filesize>=0.9",
    "click>=8.1.8",
    "rapidfuzz>=3.9.6",
    "numpy>=1.26.4",               # 1.26.4 has wheels for 3.12
    "requests>=2.32.0",
    "strsimpy>=0.2.1",
    "update-checker>=0.18.0",
    "nltk>=3.9.1",                 # needed for stopwords
]
"""
requirements_to_install = [
    'igraph==0.10.4;python_version>="3.7"',
    'python-igraph==0.9.1;python_version<"3.7"',
    'gensim==3.8.3',
    'click==7.1.2',
    'hurry.filesize==0.9',
    'kneed==0.3.1',
    'nltk==3.6.2',
    'rapidfuzz==2.11.1',
    'numpy>=1.19.5',
    'requests==2.25.1',
    'spacy==3.0.5',
    'strsimpy==0.2.0',
    'update-checker==0.18.0',
]
"""
# --- Version from config.ini (UTF-8 read) ---
config = configparser.ConfigParser()
config.read(os.path.join("cso_classifier", "config.ini"), encoding="utf-8")
__version__ = config["classifier"]["classifier_version"]

setup(
    name="cso-classifier",
    version=__version__,
    author="Angelo Salatino",
    author_email="angelo.salatino@open.ac.uk",
    description=(
        "A light-weight Python app for classifying scientific documents with "
        "the topics from the Computer Science Ontology (https://cso.kmi.open.ac.uk/home)."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/angelosalatino/cso-classifier",
    packages=find_packages(exclude=("tests", "docs", "examples")),
    include_package_data=True,
    package_data={"cso_classifier": ["assets/*", "config.ini"]},
    install_requires=requirements_to_install,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache-2.0",
    python_requires=">=3.6.0",
)
