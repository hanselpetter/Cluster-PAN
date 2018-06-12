Author Clustering using Hierarchical Clustering Analysis
==============================================================

This software was developed for the [PAN] 2017 [author clustering]
competition.

[pan]: https://pan.webis.de/clef17/pan17-web/index.html
[author clustering]: https://pan.webis.de/clef17/pan17-web/author-identification.html

You can find the paper describing our approach at
<http://ceur-ws.org/Vol-1866/paper_108.pdf>.

# Python 2.7 Requirements #

* Numpy
* Scikit-learn
* Gensim
* Scipy
* Bcubed

# Using the software #

python clusterAuthors.py -i path/to/training/corpus -o path/to/output/directory -c clusteringAlgorithm -w weightingScheme -n featuresThreshold

or

python clusterAuthors.py -h

# Please cite #

**Clustering software:**
Gómez-Adorno, H., Aleman, Y., Vilariño, D., Sanchez-Perez, M. A., Pinto, D., & Sidorov, G. Author Clustering using Hierarchical Clustering Analysis in CLEF 2017 Working Notes. CEUR Workshop Proceedings, 2017.

**Stylometric features:**
Gomez Adorno, H. M., Rios, G., Posadas Durán, J. P., Sidorov, G., & Sierra, G. (2018). Stylometry-based Approach for Detecting Writing Style Changes in Literary Texts. Computación y Sistemas, 22(1).

**Typed n-grams:**
Markov, Ilia, Efstathios Stamatatos, and Grigori Sidorov. Improving cross-topic authorship attribution: The role of pre-processing. Proceedings of the 18th International Conference on Computational Linguistics and Intelligent Text Processing. CICLing. 2017.
