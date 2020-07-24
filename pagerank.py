import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


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


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Initialize dictionary with distributions
    distribution = dict()
    # If no link on page, all pages in corpus get equal weights.
    if len(corpus[page]) == 0:
        for p in corpus:
            distribution[p] = 1/len(corpus)
    # If links on page, probability is calculated based on two steps.
    else:
        # Step 1: With probability 1 - damping_factor, any pages in the corpus
        # #   is chosen randomly.
        for p in corpus:
            distribution[p] = (1-damping_factor) * (1/len(corpus))
        # Step 2: With probability damping_factor, one of the links from page
        # is chosen randomly
        n = len(corpus[page])
        for link in corpus[page]:
            distribution[link] += damping_factor * (1/n)
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visits = dict()
    for p in corpus:
            visits[p] = 0
    sample = random.choice(list(corpus))
    counter = 0
    while counter < n:
        visits[sample] += 1
        probability = transition_model(corpus, sample, damping_factor)
        sample = random.choices(list(probability.keys()), weights=probability.values(), k=1)[0]
        counter += 1
    pagerank = {k: v / n for k, v in visits.items()}
    return pagerank 


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize pagerank dictionary that includes all pages in corpus
    pagerank = dict()
    for p in corpus:
        pagerank[p] = 1/len(corpus)
    # Iterate pagerank until change is smaller than 0.001 for all pages.
    loop_helper = 0
    while loop_helper == 0:
        pagerank_old = copy.deepcopy(pagerank)
        for p1 in corpus:
            pagerank[p1] = ((1-damping_factor)/len(corpus)) 
            for p2 in corpus:
                if p1 in corpus[p2] and p1!=p2:
                    pagerank[p1] += damping_factor * (pagerank[p2]/len(corpus[p2]))
                if len(corpus[p2]) == 0 and p1!=p2:
                    pagerank[p1] += damping_factor/len(corpus)
        difference = {key: abs(pagerank_old[key] - pagerank.get(key)) for key in pagerank_old}
        if all(x < 0.001 for x in difference.values()):
            loop_helper += 1
    total = sum(pagerank.values())
    # Scale value to make sure they add up to 1
    pagerank = {k: v / total for k, v in pagerank.items()}
    return pagerank


if __name__ == "__main__":
    main()
