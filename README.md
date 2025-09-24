# CSO-Classifier

[![PyPI version](https://badge.fury.io/py/cso-classifier.svg)](https://badge.fury.io/py/cso-classifier) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2660819.svg)](https://doi.org/10.5281/zenodo.2660819)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Abstract

Classifying research papers according to their research topics is an important task to improve their retrievability, assist the creation of smart analytics, and support a variety of approaches for analysing and making sense of the research environment. In this repository, we present the CSO Classifier, a new unsupervised approach for automatically classifying research papers according to the [Computer Science Ontology (CSO)](https://cso.kmi.open.ac.uk), a comprehensive ontology of research areas in the field of Computer Science. The CSO Classifier takes as input the metadata associated with a research paper (title, abstract, keywords) and returns a selection of research concepts drawn from the ontology. The approach was evaluated on a gold standard of manually annotated articles yielding a significant improvement over alternative methods.

Read more: [https://skm.kmi.open.ac.uk/cso-classifier/](https://skm.kmi.open.ac.uk/cso-classifier/)

## Table of contents

<!--ts-->
- [CSO-Classifier](#cso-classifier)
  - [Abstract](#abstract)
  - [Table of contents](#table-of-contents)
  - [About](#about)
  - [Getting started](#getting-started)
    - [Installation using PIP](#installation-using-pip)
    - [Installation using Github](#installation-using-github)
    - [Troubleshooting](#troubleshooting)
      - [Unable to install requirements](#unable-to-install-requirements)
      - [Unable to install python-Levenshtein](#unable-to-install-python-levenshtein)
      - ["python setup.py egg\_info" failed](#python-setuppy-egg_info-failed)
    - [Setup](#setup)
    - [Update](#update)
    - [Version](#version)
    - [Test](#test)
  - [Usage examples](#usage-examples)
    - [Classifying a single paper (SP)](#classifying-a-single-paper-sp)
      - [Sample Input (SP)](#sample-input-sp)
      - [Run (SP)](#run-sp)
      - [Sample Output (SP)](#sample-output-sp)
      - [Run on Single Paper with filter\_by](#run-on-single-paper-with-filter_by)
      - [Sample Output when using the filter\_by parameter](#sample-output-when-using-the-filter_by-parameter)
    - [Classifying in batch mode (BM)](#classifying-in-batch-mode-bm)
      - [Sample Input (BM)](#sample-input-bm)
      - [Run (BM)](#run-bm)
      - [Sample Output (BM)](#sample-output-bm)
    - [Parameters](#parameters)
  - [Releases](#releases)
    - [v3.3](#v33)
    - [v3.2](#v32)
    - [v3.1](#v31)
    - [v3.0](#v30)
    - [v2.3.2](#v232)
    - [v2.3.1](#v231)
    - [v2.3](#v23)
    - [v2.2](#v22)
    - [v2.1](#v21)
    - [v2.0](#v20)
    - [v1.0](#v10)
  - [List of Files](#list-of-files)
  - [Word2vec model and token-to-cso-combined file generation](#word2vec-model-and-token-to-cso-combined-file-generation)
    - [Word Embedding generation](#word-embedding-generation)
    - [token-to-cso-combined file](#token-to-cso-combined-file)
  - [Use the CSO Classifier in other domains of Science](#use-the-cso-classifier-in-other-domains-of-science)
  - [How to Cite CSO Classifier](#how-to-cite-cso-classifier)
  - [License](#license)
  - [References](#references)
<!--te-->

## About

The CSO Classifier is a novel application that takes as input the text from the abstract, title, and keywords of a research paper and outputs a list of relevant concepts from CSO. It consists of three main components: (i) the syntactic module, (ii) the semantic module and (iii) the post-processing module. Figure 1 depicts its architecture. The syntactic module parses the input documents and identifies CSO concepts that are explicitly referred to in the document. The semantic module uses part-of-speech tagging to identify promising terms and then exploits word embeddings to infer semantically related topics. Finally, the post-processing module combines the results of these two modules, removes outliers, and enhances them by including relevant super-areas.

![Framework of CSO Classifier](https://github.com/angelosalatino/cso-classifier/raw/master/images/Workflow.png "Framework of CSO Classifier")
**Figure 1**: Framework of CSO Classifier

## Getting started

### Installation using PIP

1. Ensure you have **Python 3.11.0**,**Python 3.12.0**, or recent. Download them [from here](https://www.python.org/downloads/). Perhaps, you may want to use a virtual environment. Here is how to [create and activate](https://docs.python.org/3/tutorial/venv.html) a virtual environment.
2. Use pip to install the classifier: ```pip install cso-classifier```
3. Setting up the classifier. Go to [Setup](#setup) for finalising the installation.

### Installation using Github

1. Ensure you have **Python 3.11.0**, or recent. Download them [from here](https://www.python.org/downloads/). Perhaps, you may want to use a virtual environment. Here is how to [create and activate](https://docs.python.org/3/tutorial/venv.html) a virtual environment.
2. Download this repository using: ```git clone https://github.com/angelosalatino/cso-classifier.git```
3. Install the package by running the following command: ```pip install ./cso-classifier```
4. Setting up the classifier. Go to [Setup](#setup) for finalising the installation.

### Troubleshooting

Although, we have worked hard to fix many issues occurring at testing phase, some of them could still arise for reasons that go beyond our control. Here is the list of the common issues we have encountered.

#### Unable to install requirements

Most likely this issue is due to the version of ```pip``` you are currently using. Make sure to update to the latest version of pip: ```pip install --upgrade pip```.

#### Unable to install python-Levenshtein

Many users found difficulties in installing the python-Levenshtein library on some Linux servers. One way to get around this issue is to install the ```python3-devel``` package. You might need sudo rights on the hosting machine.

-- Special thanks to Panagiotis Mavridis for suggesting the solution.

#### "python setup.py egg_info" failed

More specifically: ```Command "python setup.py egg_info" failed with error code 1```. This error is due to the *setup.py* file. The occurrence of this issue is rare. If you are experiencing it, please do get in touch with us. We will work with you to fix it.

### Setup

After installing the CSO Classifier, it is important to set it up with the right dependencies. To set up the classifier, please run the following code:

```python
from cso_classifier import CSOClassifier as cc
cc.setup()
exit() # it is important to close the current console, to make those changes effective
```

This function downloads the English package of spaCy, which is equivalent to run ```python -m spacy download en_core_web_sm```.
Then, it downloads the latest version of Computer Science Ontology and the latest version of the word2vec model, which will be used across all modules.

### Update

This functionality allows to update both ontology and word2vec model.

```python
from cso_classifier import CSOClassifier as cc
cc.update()

#or
cc.update(force = True)
```

By just running ```update()``` without parameters, the system will check the version of the ontology/model that is currently using, against the lastest available version. The update will be performed if one of the two or both are outdated.
Instead with ```update(force = True)``` the system will force the update by deleting the ontology/model that is currently using, and downloading their latest version.

### Version

This functionality returns the version of the CSO Classifier and CSO ontology you are currently using. It will also check online if there is a newer version, for both of them, and suggest how to update.

```python
from cso_classifier import CSOClassifier as cc
cc.version()
```

Instead, if you just want to know the package version use:
```python
import cso_classifier
print(cso_classifier.__version__)
```

### Test

This functionality allows you to test whether the classifier has been properly installed.

```python
import cso_classifier as test
test.test_classifier_single_paper() # to test it with one paper
test.test_classifier_batch_mode() # to test it with multiple papers
```

To ensure that the classifier has been installed successfully, these two functions ```test_classifier_single_paper()``` and ```test_classifier_batch_mode()``` print out both paper(s) info and the result of their classification.

## Usage examples

In this section, we explain how to run the CSO Classifier to classify a single or multiple (_batch mode_) papers.

### Classifying a single paper (SP)

#### Sample Input (SP)

The sample input can be either a *dictionary* containing title, abstract and keywords as keys, or a *string*:
```json
paper = {
        "title": "De-anonymizing Social Networks",
        "abstract": "Operators of online social networks are increasingly sharing potentially "
            "sensitive information about users and their relationships with advertisers, application "
            "developers, and data-mining researchers. Privacy is typically protected by anonymization, "
            "i.e., removing names, addresses, etc. We present a framework for analyzing privacy and "
            "anonymity in social networks and develop a new re-identification algorithm targeting "
            "anonymized social-network graphs. To demonstrate its effectiveness on real-world networks, "
            "we show that a third of the users who can be verified to have accounts on both Twitter, a "
            "popular microblogging service, and Flickr, an online photo-sharing site, can be re-identified "
            "in the anonymous Twitter graph with only a 12% error rate. Our de-anonymization algorithm is "
            "based purely on the network topology, does not require creation of a large number of dummy "
            "\"sybil\" nodes, is robust to noise and all existing defenses, and works even when the overlap "
            "between the target network and the adversary's auxiliary information is small.",
        "keywords": "data mining, data privacy, graph theory, social networking (online)"
        }

#or

paper = """De-anonymizing Social Networks
Operators of online social networks are increasingly sharing potentially sensitive information about users and their relationships with advertisers, application developers, and data-mining researchers. Privacy is typically protected by anonymization, i.e., removing names, addresses, etc. We present a framework for analyzing privacy and anonymity in social networks and develop a new re-identification algorithm targeting anonymized social-network graphs. To demonstrate its effectiveness on real-world networks, we show that a third of the users who can be verified to have accounts on both Twitter, a popular microblogging service, and Flickr, an online photo-sharing site, can be re-identified in the anonymous Twitter graph with only a 12% error rate. Our de-anonymization algorithm is based purely on the network topology, does not require creation of a large number of dummy "sybil" nodes, is robust to noise and all existing defenses, and works even when the overlap between the target network and the adversary's auxiliary information is small.
data mining, data privacy, graph theory, social networking (online)"""
```

In case the input variable is a *dictionary*, the classifier checks only the fields ```title```, ```abstract``` and ```keywords```. However, there is no need for filling all three of them. Indeed, if for instance you do not have *keywords*, you can just use the *title* and *abstract*.

#### Run (SP)

Just import the classifier and run it:

```python
from cso_classifier import CSOClassifier
cc = CSOClassifier(modules = "both", enhancement = "first", explanation = True)
result = cc.run(paper)
print(result)
```

To observe the available settings please refer to the [Parameters](#parameters) section.

If you have more than one paper to classify, you can use the following example:

```python
from cso_classifier import CSOClassifier
cc = CSOClassifier(modules = "both", enhancement = "first", explanation = True)
results = list()
for paper in papers:
  results.append(cc.run(paper))
print(results)
```

Even if you are running multiple classifications, the current implementation of the CSO Classifier will load the CSO and the model only once, saving computational time.

#### Sample Output (SP)

As output, the classifier returns a dictionary with seven components: (i) syntactic, (ii) semantic, (iii) union, (iv) enhanced, (v) explanation, (vi) syntactic_weights and (vii) semantic_weights. The explanation field is available only if the **explanation** flag is set to True. The last two fields are available only if the **get_weights** is set to True.

Below you can find an example. The keys syntactic and semantic respectively contain the topics returned by the syntactic and semantic module. Union contains the unique topics found by the previous two modules. In enhanced you can find the relevant super-areas. For the sake of clarity, we run the example with all the flag on, and hence it contains the enhanced field and both syntactic_weights and semantic_weights.

*Please be aware that the results may change according to the version of Computer Science Ontology.*

```json
{
    "syntactic": [
        "social networks",
        "anonymity",
        "graph theory",
        "sensitive informations",
        "anonymization",
        "twitter",
        "micro-blog",
        "privacy",
        "online social networks",
        "data mining",
        "data privacy",
        "network topology",
        "real-world networks"
    ],
    "semantic": [
        "anonymous communication",
        "social networks",
        "social media",
        "bipartite graphs",
        "micro-blog",
        "anonymity",
        "graph theory",
        "anonymization",
        "twitter",
        "online communities",
        "topology",
        "privacy",
        "online social networks",
        "data mining",
        "social networking sites",
        "data privacy",
        "association rules",
        "network topology",
        "network architecture"
    ],
    "union": [
        "anonymous communication",
        "social networks",
        "social media",
        "bipartite graphs",
        "topology",
        "sensitive informations",
        "micro-blog",
        "privacy",
        "online social networks",
        "data mining",
        "social networking sites",
        "real-world networks",
        "anonymity",
        "graph theory",
        "anonymization",
        "twitter",
        "data privacy",
        "online communities",
        "association rules",
        "network topology",
        "network architecture"
    ],
    "enhanced": [
        "communication",
        "communication systems",
        "world wide web",
        "access control",
        "network security",
        "computer security",
        "online systems",
        "computer science",
        "complex networks",
        "authentication",
        "theoretical computer science",
        "privacy preserving",
        "computer networks"
    ],
    "explanation": {
        "social networks": [
            "social networking",
            "microblogging",
            "social networks",
            "twitter graph",
            "social-network",
            "social network",
            "anonymous twitter",
            "twitter",
            "online social networks",
            "real-world networks"
        ],
        "online social networks": [
            "social networks",
            "social network",
            "online social networks"
        ],
        "sensitive informations": [
            "sensitive information"
        ],
        "data mining": [
            "mining",
            "data mining",
            "mining researchers",
            "data-mining"
        ],
        "privacy": [
            "anonymous",
            "anonymity",
            "anonymous twitter",
            "data privacy",
            "privacy",
            "sensitive information"
        ],
        "anonymization": [
            "anonymization"
        ],
        "anonymity": [
            "anonymous twitter",
            "anonymous",
            "anonymity"
        ],
        "real-world networks": [
            "real-world networks"
        ],
        "twitter": [
            "anonymous twitter",
            "microblogging",
            "twitter",
            "twitter graph"
        ],
        "micro-blog": [
            "anonymous twitter",
            "microblogging",
            "twitter",
            "twitter graph"
        ],
        "network topology": [
            "network topology",
            "topology"
        ],
        "data privacy": [
            "privacy",
            "data privacy"
        ],
        "graph theory": [
            "graphs",
            "graph",
            "graph theory",
            "network graphs"
        ],
        "topology": [
            "network topology",
            "topology"
        ],
        "network architecture": [
            "world networks",
            "networks",
            "network"
        ],
        "social networking sites": [
            "social networking",
            "social networks",
            "social network",
            "online social networks"
        ],
        "association rules": [
            "data mining",
            "mining researchers",
            "mining"
        ],
        "social media": [
            "social networking",
            "microblogging",
            "social networks",
            "twitter graph",
            "anonymous twitter",
            "twitter"
        ],
        "online communities": [
            "social networks",
            "social network",
            "online social networks"
        ],
        "anonymous communication": [
            "anonymous twitter",
            "anonymity",
            "anonymous"
        ],
        "bipartite graphs": [
            "graphs",
            "graph",
            "network graphs"
        ],
        "communication": [
            "anonymous twitter",
            "anonymity",
            "anonymous"
        ],
        "communication systems": [
            "anonymous twitter",
            "anonymity",
            "anonymous"
        ],
        "world wide web": [
            "social networking",
            "social networks",
            "twitter",
            "online social networks",
            "social-network",
            "social network"
        ],
        "access control": [
            "sensitive information"
        ],
        "network security": [
            "anonymous twitter",
            "anonymous",
            "anonymity",
            "sensitive information"
        ],
        "computer security": [
            "anonymous twitter",
            "anonymous",
            "data privacy",
            "privacy",
            "anonymity",
            "sensitive information"
        ],
        "online systems": [
            "social networks",
            "online social networks",
            "social network"
        ],
        "computer science": [
            "data mining",
            "data-mining",
            "mining"
        ],
        "complex networks": [
            "real-world networks"
        ],
        "authentication": [
            "anonymous twitter",
            "anonymous",
            "anonymity"
        ],
        "theoretical computer science": [
            "graphs",
            "graph",
            "graph theory",
            "network graphs"
        ],
        "privacy preserving": [
            "anonymization"
        ],
        "computer networks": [
            "world networks",
            "networks",
            "network",
            "network topology",
            "topology"
        ]
    },
    "syntactic_weights": {
        "social networks": 1.0,
        "online social networks": 1.0,
        "sensitive informations": 0.9545454545454546,
        "data mining": 1.0,
        "privacy": 1.0,
        "anonymization": 1.0,
        "anonymity": 1.0,
        "real-world networks": 1.0,
        "twitter": 1.0,
        "micro-blog": 1.0,
        "network topology": 1.0,
        "data privacy": 1.0,
        "graph theory": 1.0
    },
    "semantic_weights": {
        "social networks": 1.0,
        "online social networks": 1.0,
        "data mining": 1.0,
        "privacy": 1.0,
        "data privacy": 1.0,
        "anonymization": 1.0,
        "anonymity": 1.0,
        "twitter": 1.0,
        "network topology": 1.0,
        "topology": 1.0,
        "graph theory": 1.0,
        "network architecture": 0.75,
        "social networking sites": 0.5833333333333334,
        "association rules": 0.4375,
        "social media": 0.375,
        "micro-blog": 0.375,
        "online communities": 0.3125,
        "anonymous communication": 0.3125,
        "bipartite graphs": 0.3125
    },
    "filtered_syntactic": [
        "anonymity",
        "sensitive informations",
        "anonymization",
        "privacy",
        "data privacy"
    ],
    "filtered_semantic": [
        "anonymous communication",
        "anonymity",
        "anonymization",
        "privacy",
        "data privacy"
    ],
    "filtered_union": [
        "anonymous communication",
        "sensitive informations",
        "privacy",
        "anonymity",
        "anonymization",
        "data privacy"
    ],
    "filtered_enhanced": [
        "access control",
        "network security",
        "computer security",
        "authentication",
        "privacy preserving"
    ]
}

```

#### Run on Single Paper with filter_by

In this example, we will run the CSO Classifier by filtering topics in *computer security* (look at how the ```filter_by``` parameter is set).

```python
from cso_classifier import CSOClassifier
cc = CSOClassifier(modules = "both", enhancement = "first", explanation = True, filter_by=["computer security"])
result = cc.run(paper)
print(result)
```

#### Sample Output when using the filter_by parameter

The JSON below it the produced output, and as you can see there 4 additional keys (*filtered_XXXX*) at the bottom containing only a subset of topics within the field of **computer security**.

```json
{
    "syntactic": [
        "sensitive informations",
        "social networks",
        "micro-blog",
        "real-world networks",
        "data mining",
        "twitter",
        "network topology",
        "graph theory",
        "online social networks",
        "anonymization",
        "anonymity",
        "data privacy",
        "privacy"
    ],
    "semantic": [
        "unlinkability",
        "graph theory",
        "user information",
        "anonymity",
        "social network sites",
        "facebook",
        "individual privacy",
        "big data",
        "social networking sites",
        "user privacy",
        "optimization problems",
        "privacy",
        "anonymous communication",
        "connected graph",
        "graph structures",
        "communication networks",
        "network topology",
        "user-generated content",
        "online social networks",
        "online communities",
        "hybrid algorithms",
        "source nodes",
        "data mining",
        "privacy protection",
        "weighted graph",
        "data privacy",
        "gateway nodes",
        "social graphs",
        "system theory",
        "security and privacy",
        "routing scheme",
        "knowledge discovery in database",
        "web mining",
        "social relationships",
        "complex network theory",
        "social networks",
        "software frameworks",
        "internet",
        "privacy and security",
        "topology",
        "topological structure",
        "k-anonymity",
        "online social networkings",
        "web content",
        "combinatorial mathematics",
        "particle swarm optimization (pso)",
        "privacy preserving",
        "data mining techniques",
        "network components",
        "untraceability",
        "integrated data",
        "service management",
        "twitter",
        "data protection",
        "intermediate node",
        "formal framework",
        "association rules",
        "mining process",
        "social computing",
        "text mining",
        "social aspect",
        "network architecture",
        "digraph",
        "personal privacy",
        "spanning tree",
        "social relations",
        "adaptive algorithms",
        "directed graphs",
        "knowledge discovery",
        "online learning",
        "information privacy",
        "mesh network",
        "general graph",
        "micro-blog",
        "data security",
        "bipartite graphs",
        "association mining",
        "anonymization",
        "data anonymization",
        "privacy concerns",
        "social media",
        "social network services"
    ],
    "union": [
        "k-anonymity",
        "unlinkability",
        "graph theory",
        "user information",
        "anonymity",
        "online social networkings",
        "web content",
        "social network sites",
        "sensitive informations",
        "facebook",
        "combinatorial mathematics",
        "individual privacy",
        "big data",
        "social networking sites",
        "user privacy",
        "particle swarm optimization (pso)",
        "optimization problems",
        "privacy preserving",
        "data mining techniques",
        "network components",
        "privacy",
        "untraceability",
        "anonymous communication",
        "integrated data",
        "service management",
        "twitter",
        "data protection",
        "intermediate node",
        "connected graph",
        "formal framework",
        "association rules",
        "graph structures",
        "communication networks",
        "mining process",
        "network topology",
        "user-generated content",
        "social computing",
        "online social networks",
        "text mining",
        "online communities",
        "hybrid algorithms",
        "network architecture",
        "social aspect",
        "digraph",
        "real-world networks",
        "source nodes",
        "data mining",
        "privacy protection",
        "weighted graph",
        "personal privacy",
        "data privacy",
        "spanning tree",
        "social relations",
        "gateway nodes",
        "adaptive algorithms",
        "directed graphs",
        "knowledge discovery",
        "online learning",
        "information privacy",
        "mesh network",
        "social graphs",
        "general graph",
        "system theory",
        "micro-blog",
        "data security",
        "bipartite graphs",
        "security and privacy",
        "routing scheme",
        "knowledge discovery in database",
        "association mining",
        "anonymization",
        "web mining",
        "social relationships",
        "complex network theory",
        "social networks",
        "software frameworks",
        "data anonymization",
        "internet",
        "privacy and security",
        "privacy concerns",
        "social media",
        "topology",
        "topological structure",
        "social network services"
    ],
    "enhanced": [
        "database systems",
        "electronic document identification systems",
        "theoretical computer science",
        "recommender systems",
        "personal information",
        "authentication",
        "network security",
        "world wide web",
        "access control",
        "digital storage",
        "optimization",
        "swarm intelligence",
        "correlation analysis",
        "program compilers",
        "computer security",
        "communication",
        "communication systems",
        "data integration",
        "network management",
        "quality of service",
        "telecommunication services",
        "information technology",
        "cryptography",
        "wireless networks",
        "ad hoc networks",
        "sensor networks",
        "wireless sensor networks",
        "network coding",
        "routing protocols",
        "graph g",
        "formal methods",
        "graphic methods",
        "computer networks",
        "telecommunication networks",
        "web 2.0",
        "user interfaces",
        "ubiquitous computing",
        "interactive computer systems",
        "human engineering",
        "online systems",
        "text processing",
        "evolutionary algorithms",
        "sociology",
        "complex networks",
        "computer science",
        "gateways (computer networks)",
        "software",
        "knowledge acquisition",
        "information dissemination",
        "information systems",
        "wireless mesh networks (wmn)",
        "approximation algorithms",
        "artificial intelligence",
        "security systems",
        "routing algorithms",
        "associative processing",
        "search engines",
        "computer programming"
    ],
    "explanation": {
        "social networks": [
            "social networks",
            "real-world networks",
            "social network",
            "twitter",
            "social networking",
            "social",
            "online social networks",
            "social-network"
        ],
        "online social networks": [
            "online social networks",
            "social networks",
            "social network",
            "social networking"
        ],
        "sensitive informations": [
            "sensitive information"
        ],
        "data mining": [
            "data mining",
            "mining",
            "anonymization",
            "data privacy",
            "data-mining",
            "mining researchers",
            "privacy"
        ],
        "privacy": [
            "privacy",
            "anonymous twitter",
            "anonymization",
            "anonymity",
            "anonymous",
            "data privacy",
            "sensitive information"
        ],
        "anonymization": [
            "anonymization"
        ],
        "anonymity": [
            "anonymous twitter",
            "anonymity",
            "anonymous"
        ],
        "real-world networks": [
            "real-world networks"
        ],
        "twitter": [
            "anonymous twitter",
            "microblogging",
            "twitter graph",
            "twitter"
        ],
        "micro-blog": [
            "twitter graph",
            "twitter",
            "anonymous twitter",
            "microblogging"
        ],
        "network topology": [
            "network topology",
            "topology"
        ],
        "data privacy": [
            "data privacy",
            "privacy"
        ],
        "graph theory": [
            "network graphs",
            "graph",
            "graphs",
            "graph theory"
        ],
        "topology": [
            "network topology",
            "topology"
        ],
        "network architecture": [
            "network",
            "world networks",
            "networks"
        ],
        "social networking sites": [
            "online social networks",
            "social networks",
            "social network",
            "social networking"
        ],
        "association rules": [
            "data mining",
            "mining",
            "mining researchers"
        ],
        "social media": [
            "social networks",
            "social networking",
            "twitter",
            "social"
        ],
        "online communities": [
            "online social networks",
            "social networks",
            "social network"
        ],
        "anonymous communication": [
            "anonymous",
            "anonymous twitter",
            "anonymity"
        ],
        "bipartite graphs": [
            "network graphs",
            "graphs",
            "graph"
        ],
        "individual privacy": [
            "data privacy",
            "privacy"
        ],
        "social relationships": [
            "social network",
            "social"
        ],
        "social graphs": [
            "social networks",
            "social network"
        ],
        "social network services": [
            "online social networks",
            "social networks"
        ],
        "knowledge discovery": [
            "data mining",
            "mining"
        ],
        "privacy protection": [
            "data privacy",
            "privacy"
        ],
        "privacy and security": [
            "data privacy",
            "privacy"
        ],
        "user privacy": [
            "data privacy",
            "privacy"
        ],
        "privacy concerns": [
            "data privacy",
            "privacy"
        ],
        "data protection": [
            "data privacy",
            "privacy"
        ],
        "privacy preserving": [
            "anonymization",
            "data privacy",
            "privacy"
        ],
        "directed graphs": [
            "graphs",
            "graph"
        ],
        "weighted graph": [
            "graphs",
            "graph"
        ],
        "facebook": [
            "twitter",
            "social networking"
        ],
        "social relations": [
            "social"
        ],
        "social computing": [
            "social"
        ],
        "social aspect": [
            "social"
        ],
        "communication networks": [
            "networks"
        ],
        "mesh network": [
            "networks"
        ],
        "knowledge discovery in database": [
            "data mining"
        ],
        "online social networkings": [
            "social network",
            "social networking"
        ],
        "integrated data": [
            "data"
        ],
        "personal privacy": [
            "privacy"
        ],
        "security and privacy": [
            "privacy"
        ],
        "information privacy": [
            "privacy"
        ],
        "network components": [
            "network"
        ],
        "online learning": [
            "online"
        ],
        "user information": [
            "information"
        ],
        "web content": [
            "users"
        ],
        "data mining techniques": [
            "data mining"
        ],
        "text mining": [
            "data mining"
        ],
        "big data": [
            "data mining"
        ],
        "web mining": [
            "data mining"
        ],
        "association mining": [
            "mining"
        ],
        "mining process": [
            "mining"
        ],
        "k-anonymity": [
            "anonymization"
        ],
        "data anonymization": [
            "anonymization"
        ],
        "unlinkability": [
            "anonymity"
        ],
        "adaptive algorithms": [
            "algorithm"
        ],
        "hybrid algorithms": [
            "algorithm"
        ],
        "optimization problems": [
            "algorithm"
        ],
        "particle swarm optimization (pso)": [
            "algorithm"
        ],
        "general graph": [
            "graph"
        ],
        "software frameworks": [
            "framework"
        ],
        "formal framework": [
            "framework"
        ],
        "untraceability": [
            "anonymity"
        ],
        "digraph": [
            "graphs"
        ],
        "graph structures": [
            "graphs"
        ],
        "spanning tree": [
            "graphs"
        ],
        "connected graph": [
            "graphs"
        ],
        "service management": [
            "service"
        ],
        "routing scheme": [
            "network topology"
        ],
        "topological structure": [
            "topology"
        ],
        "gateway nodes": [
            "nodes"
        ],
        "source nodes": [
            "nodes"
        ],
        "intermediate node": [
            "nodes"
        ],
        "data security": [
            "data privacy"
        ],
        "combinatorial mathematics": [
            "graph theory"
        ],
        "complex network theory": [
            "graph theory"
        ],
        "system theory": [
            "theory"
        ],
        "user-generated content": [
            "social networking"
        ],
        "internet": [
            "social networking"
        ],
        "social network sites": [
            "social networking"
        ],
        "database systems": [
            "data mining",
            "mining",
            "anonymization"
        ],
        "electronic document identification systems": [
            "anonymity"
        ],
        "theoretical computer science": [
            "graph theory"
        ],
        "recommender systems": [
            "information"
        ],
        "personal information": [
            "privacy",
            "information"
        ],
        "authentication": [
            "anonymous twitter",
            "anonymity",
            "anonymous",
            "data privacy",
            "privacy"
        ],
        "network security": [
            "anonymous twitter",
            "anonymity",
            "anonymous",
            "data privacy",
            "privacy",
            "sensitive information"
        ],
        "world wide web": [
            "social networks",
            "real-world networks",
            "social network",
            "social networking",
            "twitter",
            "social",
            "users",
            "online social networks",
            "social-network"
        ],
        "access control": [
            "data privacy",
            "privacy",
            "sensitive information"
        ],
        "digital storage": [
            "data mining"
        ],
        "optimization": [
            "algorithm"
        ],
        "swarm intelligence": [
            "algorithm"
        ],
        "correlation analysis": [
            "algorithm"
        ],
        "program compilers": [
            "network"
        ],
        "computer security": [
            "sensitive information",
            "anonymous twitter",
            "anonymization",
            "anonymity",
            "anonymous",
            "data privacy",
            "privacy"
        ],
        "communication": [
            "anonymous",
            "anonymous twitter",
            "networks",
            "anonymity"
        ],
        "communication systems": [
            "anonymous",
            "anonymous twitter",
            "anonymity"
        ],
        "data integration": [
            "data"
        ],
        "network management": [
            "service"
        ],
        "quality of service": [
            "service"
        ],
        "telecommunication services": [
            "service"
        ],
        "information technology": [
            "service"
        ],
        "cryptography": [
            "data privacy",
            "privacy"
        ],
        "wireless networks": [
            "nodes"
        ],
        "ad hoc networks": [
            "nodes"
        ],
        "sensor networks": [
            "nodes"
        ],
        "wireless sensor networks": [
            "nodes"
        ],
        "network coding": [
            "nodes"
        ],
        "routing protocols": [
            "nodes",
            "network topology"
        ],
        "graph g": [
            "graphs",
            "graph"
        ],
        "formal methods": [
            "framework"
        ],
        "graphic methods": [
            "graphs",
            "graph"
        ],
        "computer networks": [
            "world networks",
            "network",
            "networks",
            "network topology",
            "topology"
        ],
        "telecommunication networks": [
            "networks"
        ],
        "web 2.0": [
            "social networking"
        ],
        "user interfaces": [
            "social networking"
        ],
        "ubiquitous computing": [
            "social"
        ],
        "interactive computer systems": [
            "social"
        ],
        "human engineering": [
            "social"
        ],
        "online systems": [
            "social networks",
            "social network",
            "online",
            "social networking",
            "social",
            "online social networks"
        ],
        "text processing": [
            "data mining"
        ],
        "evolutionary algorithms": [
            "algorithm"
        ],
        "sociology": [
            "social"
        ],
        "complex networks": [
            "real-world networks",
            "graph theory"
        ],
        "computer science": [
            "data mining",
            "mining",
            "social networking",
            "anonymization",
            "data privacy",
            "data-mining",
            "mining researchers",
            "privacy"
        ],
        "gateways (computer networks)": [
            "nodes"
        ],
        "software": [
            "algorithm"
        ],
        "knowledge acquisition": [
            "data mining",
            "mining"
        ],
        "information dissemination": [
            "privacy"
        ],
        "information systems": [
            "privacy"
        ],
        "wireless mesh networks (wmn)": [
            "networks"
        ],
        "approximation algorithms": [
            "graph"
        ],
        "artificial intelligence": [
            "theory"
        ],
        "security systems": [
            "privacy"
        ],
        "routing algorithms": [
            "network topology"
        ],
        "associative processing": [
            "mining"
        ],
        "search engines": [
            "data mining"
        ],
        "computer programming": [
            "framework"
        ]
    },
    "filtered_syntactic": [
        "sensitive informations",
        "anonymization",
        "anonymity",
        "data privacy",
        "privacy"
    ],
    "filtered_semantic": [
        "unlinkability",
        "user information",
        "anonymity",
        "individual privacy",
        "user privacy",
        "privacy",
        "anonymous communication",
        "privacy protection",
        "data privacy",
        "security and privacy",
        "privacy and security",
        "k-anonymity",
        "privacy preserving",
        "untraceability",
        "data protection",
        "personal privacy",
        "information privacy",
        "data security",
        "anonymization",
        "data anonymization",
        "privacy concerns"
    ],
    "filtered_union": [
        "k-anonymity",
        "unlinkability",
        "user information",
        "anonymity",
        "sensitive informations",
        "individual privacy",
        "user privacy",
        "privacy preserving",
        "privacy",
        "untraceability",
        "anonymous communication",
        "data protection",
        "privacy protection",
        "personal privacy",
        "data privacy",
        "information privacy",
        "data security",
        "security and privacy",
        "anonymization",
        "data anonymization",
        "privacy and security",
        "privacy concerns"
    ],
    "filtered_enhanced": [
        "electronic document identification systems",
        "personal information",
        "authentication",
        "network security",
        "access control",
        "computer security",
        "cryptography",
        "security systems"
    ]
}
```

### Classifying in batch mode (BM)

#### Sample Input (BM)

The sample input is a *dictionary* of papers. Each key is an identifier (example id1, see below) and its value is either a *dictionary* containing title, abstract and keywords as keys, or a *string*, as shown for [Classifying a single paper (SP)](#classifying-a-single-paper-sp).

```json
papers = {
    "id1": {
        "title": "De-anonymizing Social Networks",
        "abstract": "Operators of online social networks are increasingly sharing potentially sensitive information about users and their relationships with advertisers, application developers, and data-mining researchers. Privacy is typically protected by anonymization, i.e., removing names, addresses, etc. We present a framework for analyzing privacy and anonymity in social networks and develop a new re-identification algorithm targeting anonymized social-network graphs. To demonstrate its effectiveness on real-world networks, we show that a third of the users who can be verified to have accounts on both Twitter, a popular microblogging service, and Flickr, an online photo-sharing site, can be re-identified in the anonymous Twitter graph with only a 12% error rate. Our de-anonymization algorithm is based purely on the network topology, does not require creation of a large number of dummy \"sybil\" nodes, is robust to noise and all existing defenses, and works even when the overlap between the target network and the adversary's auxiliary information is small.",
        "keywords": "data mining, data privacy, graph theory, social networking (online)"
    },
    "id2": {
        "title": "Title of sample paper id2",
        "abstract": "Abstract of sample paper id2",
        "keywords": "keyword1, keyword2, ..., keywordN"
    }
}
```

#### Run (BM)

Import the python script and run the classifier:

```python
from cso_classifier import CSOClassifier
cc = CSOClassifier(workers = 1, modules = "both", enhancement = "first", explanation = True)
result = cc.batch_run(papers)
print(result)
```

To observe the available settings please refer to the [Parameters](#parameters) section.

#### Sample Output (BM)

As output the classifier returns a dictionary of dictionaries. For each classified paper (identified by their id), it returns a dictionary containing five components: (i) syntactic, (ii) semantic, (iii) union, (iv) enhanced, and (v) explanation. The latter field is available only if the explanation flag is set to True.

Below you can find an example. The keys syntactic and semantic respectively contain the topics returned by the syntactic and semantic module. Union contains the unique topics found by the previous two modules. In ehancement you can find the relevant super-areas. In explanation, you can find all chunks of text that allowed the classifier to infer a given topic. *Please be aware that the results may change according to the version of Computer Science Ontology.*

```json
{
    "id1": {
	"syntactic": ["network topology", "online social networks", "real-world networks", "anonymization", "privacy", "social networks", "data privacy", "graph theory", "data mining", "sensitive informations", "anonymity", "micro-blog", "twitter"],
	"semantic": ["network topology", "online social networks", "topology", "data privacy", "social networks", "privacy", "anonymization", "graph theory", "data mining", "anonymity", "micro-blog", "twitter"],
	"union": ["network topology", "online social networks", "topology", "real-world networks", "anonymization", "privacy", "social networks", "data privacy", "graph theory", "data mining", "sensitive informations", "anonymity", "micro-blog", "twitter"],
	"enhanced": ["computer networks", "online systems", "complex networks", "privacy preserving", "computer security", "world wide web", "theoretical computer science", "computer science", "access control", "network security", "authentication", "social media"],
	"explanation": {
		"social networks": ["social network", "online social networks", "microblogging service", "real-world networks", "social networks", "microblogging", "social networking", "twitter graph", "anonymous twitter", "twitter"],
		"online social networks": ["online social networks", "social network", "social networks"],
		"sensitive informations": ["sensitive information"],
		"privacy": ["sensitive information", "anonymity", "anonymous", "data privacy", "privacy"],
		"anonymization": ["anonymization"],
		"anonymity": ["anonymity", "anonymous"],
		"real-world networks": ["real-world networks"],
		"twitter": ["twitter graph", "twitter", "microblogging service", "anonymous twitter", "microblogging"],
		"micro-blog": ["twitter graph", "twitter", "microblogging service", "anonymous twitter", "microblogging"],
		"network topology": ["topology", "network topology"],
		"data mining": ["data mining", "mining"],
		"data privacy": ["data privacy", "privacy"],
		"graph theory": ["graph theory"],
		"topology": ["topology", "network topology"],
		"computer networks": ["topology", "network topology"],
		"online systems": ["online social networks", "social network", "social networks"],
		"complex networks": ["real-world networks"],
		"privacy preserving": ["anonymization"],
		"computer security": ["anonymity", "data privacy", "privacy"],
		"world wide web": ["social network", "online social networks", "microblogging service", "real-world networks", "social networks", "microblogging", "social networking", "twitter graph", "anonymous twitter", "twitter"],
		"theoretical computer science": ["graph theory"],
		"computer science": ["data mining", "mining"],
		"access control": ["sensitive information"],
		"network security": ["anonymity", "sensitive information", "anonymous"],
		"authentication": ["anonymity", "anonymous"],
		"social media": ["microblogging service", "microblogging", "twitter graph", "anonymous twitter", "twitter"]
	    }
    },
    "id2": {
        "syntactic": [...],
        "semantic": [...],
        "union": [...],
        "enhanced": [...],
        "explanation": {...}
    }
}
```

### Parameters
Beside the paper(s), the function running the CSO Classifier accepts seven additional parameters: (i) **workers**, (ii) **modules**, (iii) **enhancement**, (iv) **explanation**, (v) **delete_outliers**, (vi) **fast_classification**, (vii) **silent**, and (ix) **filter_by**. There is no particular order on how to specify these paramaters. Here we explain their usage. The workers parameters is an integer (equal or greater than 1), modules and enhancement are strings that define a particular behaviour for the classifier. The explanation, delete_outliers, fast_classification, and silent parameters are booleans. Finally, filter_by is a list 

(i) The parameter *workers* defines the number of threads to run for classifying the input corpus. For instance, if ```workers = 4```, there will be 4 instances of the CSO Classifier, each one receiving a chunk (equally split) of the corpus to process. Once all processes are completed, the results will be aggregated and returned. The default value for *workers* is *1*. This parameter is available only when running the classifier in *batch mode*.

(ii) The parameter *modules* can be either "syntactic", "semantic", or "both". Using the value "syntactic", the classifier will run only the syntactic module. Using the "semantic" value, instead, the classifier will use only the semantic module. Finally, using "both", the classifier will run both syntactic and semantic modules and combine their results. The default value for *modules* is *both*.

(iii) The parameter *enhancement* can be either "first", "all", or "no". This parameter controls whether the classifier will try to infer, given a topic (e.g., Linked Data), only the direct super-topics (e.g., Semantic Web) or all its super-topics (e.g., Semantic Web, WWW, Computer Science). Using "first" as a value will infer only the direct super topics. Instead, if using "all", the classifier will infer all its super-topics. Using "no" the classifier will not perform any enhancement. The default value for *enhancement* is *first*.

(iv) The parameter *explanation* can be either *True* or *False*. This parameter defines whether the classifier should return an explanation. This explanation consists of chunks of text, coming from the input paper, that allowed the classifier to return a given topic. This supports the user in better understanding why a certain topic has been inferred. The classifier will return an explanation for all topics, even for the enhanced ones. In this case, it will join all the text chunks of all its sub-topics. The default value for *explanation* is *False*.

(v) The parameter *delete_outliers* can be either *True* or *False*. This parameter controls whether to run the outlier detection component within the post-processing module. This component improves the results by removing erroneous topics that were conceptually distant from the others. Due to their computation, users might experience slowdowns. For this reason, users can decide between good results and low computational time or improved results and slower computation. The default value for *delete_outliers* is *True*.

(vi) The parameter *fast_classification* can be either *True* or *False*. This parameter determines whether the semantic module should use the full model or the cached one. Using the full model provides slightly better results than the cached one. However, using the cached model is more than 15x faster. Read [here](#word2vec-model-and-token-to-cso-combined-file-generation) for more details about these two models. The default value for *fast_classification* is *True*.

(vii) The parameter *get_weights* can be either *True* or *False*. This determines whether the classifier returns the weights associated to the identified topics. For the syntactic topics these represent the value of string similarity (Levenshtein) of topics compared the chunks of text identified in the input text. Whereas, the weights for the semantic topics correspond to the normalised values from the topic distribution obtained from running the semantic module.

(viii) The parameter *silent* can be either *True* or *False*. This determines whether the classifier prints its progress in the console. If set to True, the classifier will be silent and will not print any output while classifying. The default value for *silent* is *False*.

(ix) The parameter *filter_by* is a list, containing CSO topic, and lets you focus the classification on specific sub-branches of CSO. For instance, to narrow down the results to subtopics within **artificial intelligence** and **semantic web** you can set ```filter_by = ["artificial intelligence", "semantic web"]```. This will produce four extra outputs (*syntactic_filtered*, *semantic_filtered*, *union_filtered*, *enhanced_filtered*) containing only the CSO topics that fall under the hierarchical structure of the specified areas. By default this parameter is an empty list, and therefore the classifier will consider all CSO topics as usual. You can check [Run on Single Paper with filter\_by](#run-on-single-paper-with-filter_by) to see how it works.



|# | Parameter  |  Single Paper | Batch Mode |
|---|---|---|---|
|i  | workers  | :x:  | :white_check_mark: |
|ii | modules  | :white_check_mark:  | :white_check_mark: |
|iii| enhancement  | :white_check_mark:  | :white_check_mark: |
|iv | explanation  | :white_check_mark:  | :white_check_mark: |
|v  |delete_outliers| :white_check_mark:  | :white_check_mark: |
|vi | fast_classification| :white_check_mark:  | :white_check_mark: |
|vii| get_weights       | :white_check_mark:  | :white_check_mark: |
|viii| silent       | :white_check_mark:  | :white_check_mark: |
|ix| filter_by       | :white_check_mark:  | :white_check_mark: |


**Table 1**: Parameters availability when using CSO Classifier


## Releases

Here we list the available releases for the CSO Classifier. These releases are available for download both from [Github](https://github.com/angelosalatino/cso-classifier/releases) and [Zenodo](http://doi.org/10.5281/zenodo.2660819).

### v3.3

This release extends version 3.2 with a new feature that lets you refine the classification process by focusing on specific areas within the Computer Science Ontology. Specifically, providing one or more topics within the parameter *filter_by* (type list), the classifier will extract the sub-branches of such CSO topics, and when classifying will narrow down the output to the only sub-topics available in those areas. This is especially helpful when you are interested in exploring specific branches of the CSO, such as identifying only the concepts related to **artificial intelligence** and **semantic web** within a given paper, and can be achieved by setting ```filter_by = ["artificial intelligence", "semantic web"]``` (see [Parameters](#parameters)). If this parameter is set, the classifier will return the standard classification results, with four extra sets of results (*syntactic_filtered*, *semantic_filtered*, *union_filtered*, *enhanced_filtered*) containing only the filtered topics. This gives users the full picture and a focused view within the chosen areas.


### v3.2

This release extends version 3.1 by supporting users in exporting the weights associated to the identified topics. If enabled, within the result of the classification, the classifier include two new keys ```syntactic_weights``` and ```semantic_weights``` which respectively contain the identified syntactic and semantic topics as keys, and their weights as values. 
This component is disabled by default and can be enabled by setting ```get_weights = True``` when calling the CSO Classifier (see [Parameters](#parameters)).

### v3.1

This release brings in two main changes. The first change is related to the library (and the code) to perform the Levenshtein similarity. Before we relied on ```python-Levenshtein``` which required ```python3-devel```. This new version uses ```rapidfuzz``` which as fast as the previous library and it is much easier to install on the various systems.
The second change is related to an updated list of dependencies. We updated some libraries including ```igraph```.

Download from:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7940877.svg)](https://doi.org/10.5281/zenodo.7940877)

### v3.0

This release welcomes some improvements under the hood. In particular:
* we refactored the code, reorganising scripts into more elegant classes
* we added functionalities to automatically setup and update the classifier to the latest version of CSO
* we added the *explanation* feature, which returns chunks of text that allowed the classifier to infer a given topic
* the syntactic module takes now advantage of Spacy POS tagger (as previously done only by semantic module)
* the grammar for the chunk parser is now more robust: ```{<JJ.*>*<HYPH>*<JJ.*>*<HYPH>*<NN.*>*<HYPH>*<NN.*>+}```

In addition, in the post-processing module, we added the *outlier detection* component. This component improves the accuracy of the result set, by removing erroneous topics that were conceptually distant from the others. This component is enabled by default and can be disabled by setting ```delete_outliers = False``` when calling the CSO Classifier (see [Parameters](#parameters)).

Please, be aware that having substantially restructured the code into classes, the way of running the classifier has changed too. Thus, if you are using a previous version of the classifier, we encourage you to update it (```pip install -U cso-classifier```) and modify your calls to the classifier, accordingly. Read our [usage examples](#usage-examples).

We would like to thank James Dunham @jamesdunham from CSET (Georgetown University) for suggesting to us how to improve the code.

More details about this version of the classifier can be found within: 
> Salatino, A., Osborne, F., & Motta, E. (2022). CSO Classifier 3.0: a Scalable Unsupervised Method for Classifying Documents in terms of Research Topics. International Journal on Digital Libraries, 1-20. [Read more](https://doi.org/10.1007/s00799-021-00305-y)


Download from:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5095422.svg)](https://doi.org/10.5281/zenodo.5095422)

### v2.3.2

Version alignement with Pypi. Similar to version 2.3.1.

Download from:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3357768.svg)](https://doi.org/10.5281/zenodo.3357768)


### v2.3.1

Bug Fix. Added some exception handles. 
**Notice:** *Please note that during the upload of this version on Pypi (python index), we encountered some issues. We can't guarantee this version will work properly. To this end, we created a new release: v2.3.2. Use this last one, please. Apologies for any inconvenience.*

### v2.3
This new release contains a bug fix and the latest version of the CSO ontology.

Bug Fix: When running in batch mode, the classifier was treating the keyword field as an array instead of a string. In this way, instead of processing keywords (separated by comma), it was processing each single letters, hence inferring wrong topics. This now has been fixed. In addition, if the keyword field is actually an array, the classifier will first 'stringify' it and then process it.

We also downloaded and packed the latest version of the CSO ontology.

Download from:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3355629.svg)](https://doi.org/10.5281/zenodo.3355629)

### v2.2
In this version (release v2.2), we (i) updated the requirements needed to run the classifier, (ii) removed all unnecessary warnings, and (iii) enabled multiprocessing. In particular, we removed all useless requirements that were installed in development mode, by cleaning the _requirements.txt_ file. 

When computing certain research papers, the classifier display warnings raised by the [kneed library](https://pypi.org/project/kneed/). Since the classifier can automatically adapt to such warnings, we decided to hide them and prevent users from being concerned about such an outcome.

This version of the classifier provides improved **scalability** through multiprocessing. Once the number of workers is set (i.e. num_workers >= 1), each worker will be given a copy of the CSO Classifier with a chunk of the corpus to process. Then, the results will be aggregated once all processes are completed. Please be aware that this function is only available in batch mode. See section [Classifying in batch mode (BM)](#classifying-in-batch-mode-bm) for more details.

Download from:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3241490.svg)](https://doi.org/10.5281/zenodo.3241490)

### v2.1
This new release (version v2.1) makes the CSO Classifier more scalable. Compared to its previous version (v2.0), the classifier relies on a cached word2vec model which connects the words within the model vocabulary directly with the CSO topics. Thanks to this cache, the classifier is able to quickly retrieve all CSO topics that could be inferred by given tokens, speeding up the processing time. In addition, this cache is lighter (~64M) compared to the actual word2vec model (~366MB), which allows saving additional time at loading time.

Thanks to this improvement the CSO Classifier is around 24x faster and can be easily run on a large corpus of scholarly data.

Download from:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2689440.svg)](https://doi.org/10.5281/zenodo.2689440)

### v2.0

The second version (v2.0) implements the CSO Classifier as described in the [about section](#about). It combines the topics of both the syntactic and semantic modules and enriches them with their super-topics. Compared to [v1.0](#v10), it adds a semantic layer that allows generating a more comprehensive result, identifying research topics that are not explicitly available in the metadata. The semantic module relies on a Word2vec model trained on over 4.5M papers in _Computer Science_. [Below](#word-embedding-generation) we show more in detail how we trained such a model. In this version of the classifier, we [pickled](https://docs.python.org/3.6/library/pickle.html) the model to speed up the process of loading into memory (~4.5 times faster).

> Salatino, A.A., Osborne, F., Thanapalasingam, T., Motta, E.: The CSO Classifier: Ontology-Driven Detection of Research Topics in Scholarly Articles. In: TPDL 2019: 23rd International Conference on Theory and Practice of Digital Libraries. Springer. [Read More](http://oro.open.ac.uk/62026/)

Download from:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2661834.svg)](https://doi.org/10.5281/zenodo.2661834)

### v1.0

The first version (v1.0) of the CSO Classifier is an implementation of the syntactic module, which was also previously used to support the semi-automatic annotation of proceedings at Springer Nature [[1]](#references). This classifier aims at syntactically match n-grams (unigrams, bigrams and trigrams) of the input document with concepts within CSO.

More details about this version of the classifier can be found within: 
> Salatino, A.A., Thanapalasingam, T., Mannocci, A., Osborne, F. and Motta, E. 2018. Classifying Research Papers with the Computer Science Ontology. ISWC-P&D-Industry-BlueSky 2018 (2018). [Read more](http://oro.open.ac.uk/55908/)

Download from:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2661834.svg)](https://doi.org/10.5281/zenodo.2661834)

## List of Files

* **CSO-Classifier.ipynb**: :page_facing_up: Python notebook for executing the classifier
* **CSO-Classifier.py**: :page_facing_up: Python script for executing the classifier
* **images**: :file_folder: folder containing some pictures, e.g., the workflow showed above
* **cso_classifier**: :file_folder: Folder containing the main functionalities of the classifier
  * **classifier.py**: :page_facing_up: class that implements the CSO Classifier
  * **syntacticmodule.py**: :page_facing_up: class that implements the syntactic module
  * **semanticmodule.py**: :page_facing_up: class that implements the semantic module
  * **postprocmodule.py**: :page_facing_up:
  * **paper.py**: :page_facing_up: class that implements the functionalities to operate on papers, such as POS tagger, grammar-based chunk parser
  * **result.py**: :page_facing_up: class that implements the functionality to operate on the results
  * **ontology.py**: :page_facing_up: class that implements the functionalities to operate on the ontology: get primary label, get topics and so on
  * **model.py**: :page_facing_up: class that implements the functionalities to operate on the word2vec model: get similar words and so on
  * **misc.py**: :page_facing_up: some miscellaneous functionalities
  * **test.py**: :page_facing_up: some test functionalities
  * **config.py**: :page_facing_up: class that implements the functionalities to operate on the config file
  * **config.ini**: :page_facing_up: config file. It contains all information about packaage, ontology and model.
  * **assets**: :file_folder: Folder containing the word2vec model and CSO
    * **cso.csv**: :page_facing_up: file containing the Computer Science Ontology in csv
    * **cso.p**: :page_facing_up: serialised file containing the Computer Science Ontology (pickled)
    * **cso_graph.p** :page_facing_up: file containing the Computer Science Ontology as an iGraph object
    * **model.p**: :page_facing_up: the trained word2vec model (pickled)
    * **token-to-cso-combined.json**: :page_facing_up: file containing the cached word2vec model. This json file contains a dictionary in which each token of the corpus vocabulary, has been mapped with the corresponding CSO topics. Below we explain how this file has been generated.

## Word2vec model and token-to-cso-combined file generation

In this section, we describe how we generated the word2vec model used within the CSO Classifier and what is the token-to-cso-combined file.

### Word Embedding generation

We applied the word2vec approach [[2,3]](#references) to a collection of text from the Microsoft Academic Graph (MAG) for generating word embeddings. MAG is a scientific knowledge base and a heterogeneous graph containing scientific publication records, citation relationships, authors, institutions, journals, conferences, and fields of study. It is the largest dataset of scholarly data publicly available, and, as of April 2021, it contains more than 250 million publications.

We first downloaded titles, and abstracts of 4,654,062 English papers in the field of Computer Science. Then we pre-processed the data by replacing spaces with underscores in all n-grams matching the CSO topic labels (e.g., “digital libraries” became “digital_libraries”) and for frequent bigrams and trigrams (e.g., “highest_accuracies”, “highly_cited_journals”). These frequent n-grams were identified by analysing combinations of words that co-occur together, as suggested in [[2]](#references) and using the parameters showed in Table 2. Indeed, while it is possible to obtain the vector of an n-gram by averaging the embedding vectors of all its words, the resulting representation usually is not as good as the one obtained by considering the n-gram as a single word during the training phase.

Finally, we trained the word2vec model using the parameters provided in Table 3. The parameters were set to these values after testing several combinations.

| min-count  |  threshold |
|---|---|
| 5  | 10  |

**Table 2**: Parameters used during the collocation words analysis


| method  |  emb. size | window size | min count cutoff |
|---|---|---|---|
| skipgram  | 128  |  10 |  10 |

**Table 3**: Parameters used for training the word2vec model.


After training the model, we obtained a **gensim.models.keyedvectors.Word2VecKeyedVectors** object weighing **366MB**. You can download the model [from here](https://cso.kmi.open.ac.uk/download/model.p).

The size of the model hindered the performance of the classifier in two ways. Firstly, it required several seconds to be loaded into memory. This was partially fixed by serialising the model file (using python pickle, see version v2.0 of CSO Classifier, ~4.5x faster). Secondly, while processing a document, the classifier needs to retrieve the top 10 similar words for all tokens, and compare them with CSO topics. In performing such an operation, the model would require several seconds, becoming a bottleneck for the classification process.

To this end, we decided to create a cached model (**token-to-cso-combined.json**) which is a dictionary that directly connects all token available in the vocabulary of the model with the CSO topics. This strategy allows to quickly retrieve all CSO topics that can be inferred by a particular token.

### token-to-cso-combined file

To generate this file, we collected all the set of words available within the vocabulary of the model. Then iterating on each word, we retrieved its top 10 similar words from the model, and we computed their Levenshtein similarity against all CSO topics. If the similarity was above 0.7, we created a record that stored all CSO topics triggered by the initial word.

## Use the CSO Classifier in other domains of Science

In order to use the CSO Classifier in other domains of Science, it is necessary to replace the two external sources mentioned in the previous section. In particular, there is a need for a comprehensive ontology or taxonomy of research areas, within the new domain, which will work as a controlled list of research topics. In addition, it is important to train a new word2vec model that fits the language model and the semantic of the terms, in this particular domain. We wrote a blog article on how to integrate knowledge from other fields of Science within the CSO Classifier.

Please read here for more info: [How to use the CSO Classifier in other domains](https://salatino.org/wp/how-to-use-the-cso-classifier-in-other-domains/)

## How to Cite CSO Classifier

We kindly ask that any published research making use of the CSO Classifier cites our paper listed below:

Salatino, A.A., Osborne, F., Thanapalasingam, T., Motta, E.: The CSO Classifier: Ontology-Driven Detection of Research Topics in Scholarly Articles. In: TPDL 2019: 23rd International Conference on Theory and Practice of Digital Libraries. Springer.

## License

[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)

## References

[1] Osborne, F., Salatino, A., Birukou, A. and Motta, E. 2016. Automatic Classification of Springer Nature Proceedings with Smart Topic Miner. The Semantic Web -- ISWC 2016. 9982 LNCS, (2016), 383–399. DOI:https://doi.org/10.1007/978-3-319-46547-0_33

[2] Mikolov, T., Chen, K., Corrado, G. and Dean, J. 2013. Efficient Estimation of Word Representations in Vector Space. (Jan. 2013).

[3] Mikolov, T., Chen, K., Corrado, G. and Dean, J. 2013. Distributed Representations of Words and Phrases and their Compositionality. Advances in neural information processing systems. 3111–3119.
