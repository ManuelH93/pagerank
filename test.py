import os
import random
import re
import sys

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    for p in corpus:
        pagerank[p] = 1/len(corpus)
    print(pagerank)
    
    part2 = 0
    for p in ('1.html', '3.html', '4.html'):
        part2 += pagerank[p]/len(corpus[p])

    pagerank['2.html'] = ((1-damping_factor)/len(corpus)) + (damping_factor * part2)

    print(pagerank)

corpus = crawl('corpus0')
print(corpus)
iterate_pagerank(corpus, 0.85)


