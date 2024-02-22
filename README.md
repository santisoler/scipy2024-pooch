# Pooch: a friend to fetch your data files

[Santiago Soler][santisoler]

| Information | |
|---|---|
| Track  | General  |


<!--

I can add an image in the submission.

The submission can be done in Markdown!

-->

## Abstract

<!--

<= 100 words

- In your abstract, be sure to include answers to some basic questions: Who is
the intended audience for your talk? What, specifically, will attendees learn
from your talk?

-->

<!--
### Brainstorming

- Intended audience:
  - package maintainers, teachers and instructors, end users.
- What will they learn:
  - Package maintainers can use Pooch to easily provide sample datasets in
    gallery examples, tutorials, user guides, etc.
  - Teachers can use Pooch to easily download data files during live coding
    classes, locally or in the cloud, while ensuring that the students have the
    correct file.

What's Pooch? Who can use it? What's is useful for? Who's using it?

-->

### v1

Pooch is a Python library that can easily download and locally cache files from
the web without any hassle. Novices can use it to simply download files
in one line of code and just focus on the data.
While package maintainers use it as an easy way to provide sample datasets to
their users, specially useful while they are learning to use the tools.
Its features, ease of use, and modularity made it popular among scientific
Python libraries like [SciPy][scipy], [scikit-image][scikit-image],
[napari][napari] and [MetPy][metpy], which depend on it for distributing sample
datasets for their gallery examples and tutorials.


### v2

Pooch is a Python library that can easily download and locally cache files from
the web without any hassle. Novices can use it to simply download files
in one line of code and focus on the data.
While package maintainers can use it to provide sample datasets
to their users, on examples and tutorials, as libraries like [SciPy][scipy],
[scikit-image][scikit-image], [napari][napari] and [MetPy][metpy] do.
During this talk we'll show you how you can use the different features that
Pooch offers and also how you can extend its capabilities by writing your own
downloaders or post-processors.



## Description

<!--
Your placement in the program will be based on reviews of your description.
This should be a roughly 500-word outline of your presentation. This outline
should concisely describe software of interest to the SciPy community, tools or
techniques for more effective computing, or how scientific Python was applied
to solve a research problem. A traditional background/motivation, methods,
results, and conclusion structure is encouraged but not required. Links to
project websites, source code repositories, figures, full papers, and evidence
of public speaking ability are encouraged.


Include links to source code, articles, blog posts, or other writing that adds
context to the presentation.

Review process:
- Would you recommend accepting this proposal (yes/no)?
- Proposal rating? (numerical score 1 to 5)
- How confident are you in your review? (numerical score 1 to 5)
- Does this abstract concisely describe software of interest to the SciPy
  community, tools or techniques for more effective computing, or how
  scientific Python was applied to solve a research problem? (numerical score
  1 to 5)
-->

<!--
### Brainstorming

- What's Pooch?
- Download and cache files without frills: `retrieve`
- Automatically check file integrity.
- Reuse that cache file.
- For package maintainers, create a `Pooch` object and `fetch` files from
  anywhere.
- Download from anywhere: FTP, Zenodo, figshare, dataverse, etc.
- Unpack archives
- Why it's useful? Why you should use it?
- Extend it however you want: write your own downloaders and post-processors.
- Who's using Pooch?

Links:

- github.com/fatiando/pooch
- www.fatiando.org/pooch
- https://doi.org/10.21105/joss.01943

-->

### v1

Pooch is a slim pure-Python library for downloading files from the web, caching
them locally and checking their integrity.
It can be used to download a single file from the web when needed, or to
handle the download of several files.

Scientific Python libraries usually need to provide some sample datasets to run
in their examples and tutorials, which allow their users to get more familiar
with the tools.
Shipping these datasets along with the software is cumbersome, and make the
packages larger than needed, specially considering that those data files are
not critical for running the software.
Alternatively, we could host them in a different location, what
introduces the need for an easy way to access them.
This is where Pooch comes handy: package maintainers can rely on it to
download and cache those files, and make sure the users received the right
file.
Python libraries like [SciPy][scipy], [scikit-image][scikit-image],
[napari][napari] and [MetPy][metpy] are currently using Pooch for managing the
download of their sample data files.

Pooch has also proven useful during live-coding tutorials and classes, in which
the audience needs to access some data files in a quick way. With Pooch they
can download those files in a single line and focus on the data itself.

For downloading a single file, Pooch offers the `pooch.retrieve()` function
that takes the URL of the desired file, and optionally its checksum hash:

```python
import pooch

file_path = pooch.retrieve(
    url="https://github.com/fatiando/pooch/raw/v1.0.0/data/tiny-data.txt",
    known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
)
```

The `pooch.retrieve()` function will download the file, compare its hash to
check its integrity, store it in the default cache folder of the OS, and return
the path to file.
Once we have the file cached in our system, every time we rerun this function
it won't re-download the file and just point to the one we already have.

Pooch is capable of downloading files from different protocols, like HTTP, FTP
and also from repositories like [Zenodo][zenodo], [figshare][figshare] and
[dataverse][dataverse] directly through their DOI (Digital Object Identifier).
For example, lets download the same file, now stored in figshare under this
DOI
[10.6084/m9.figshare.14763051.v1](https://doi.org/10.6084/m9.figshare.14763051.v1):

```python
file_path = pooch.retrieve(
    url="doi:10.6084/m9.figshare.14763051.v1/tiny-data.txt",
    known_hash="md5:70e2afd3fd7e336ae478b1e740a5f08e",
)
```

In case the downloaded file is a zip archive or a compressed file,
Pooch allows us to pass a `processor` that will unpack or decompress that file
and return the path to the files within it. For example, we can use
the `pooch.Unzip` processor to unzip downloaded files:

```python
fnames = pooch.retrieve(
    url="doi:10.5281/zenodo.4924874/store.zip",
    known_hash="md5:7008231125631739b64720d1526619ae",
    processor=pooch.Unzip(),
)
```

Package maintainers usually need to provide a way to download several files,
which may suffer changes from one version of the package to another. In this
cases we can create a `pooch.Pooch` object, which can keep record of all the
files available through a _registry_:


```python
from . import version  # the version string of your project

PUPPY = pooch.create(
    path=pooch.os_cache("mypackage"),
    base_url="https://github.com/me/mypackage/raw/{version}/data/",
    version=version,
    registry={
        "temperature.csv": "sha256:19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
        "pressure.csv": "sha256:1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
    }
)
```

And then they can provide public functions to _fetch_ these data files:

```python
import pandas as pd

def fetch_temperature_data():
    """Load sample temperature data."""
    fname = PUPPY.fetch("temperature.csv")
    return pd.read_csv(fname)

def fetch_pressure_data():
    """Load sample pressure data."""
    fname = PUPPY.fetch("pressure.csv")
    return pd.read_csv(fname)
```

Pooch has been designed to be extended, so you can write your own downloaders
and post-processors to provide solutions to particular cases that aren't
covered by the built-in tools.

Include:
- link to documentation and github repo
- link to PyCascades talk (https://www.youtube.com/watch?v=KvxBc4xUMyg)

### v2

<!--
Motivation

Why Pooch?
Maintainers needing a way to provide sample datasets.
Easy way to download and cache data files in Python.
-->

<!--
Methods?

What Pooch can do?
Maybe don't get into too many details and just mention the capabilities.
-->

<!--
Results ?

Maybe showing who's using it, and positives experiences while teaching.
-->

<!--
Conclusions

Conclude with just some final thoughts
-->



[santisoler]: https://www.santisoler.com
[metpy]: https://unidata.github.io/MetPy
[napari]: https://napari.org
[scipy]: https://scipy.org
[scikit-image]: https://scikit-image.org

