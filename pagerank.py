import os
import random
import re
import sys
import numpy
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000


def main():
    #if len(sys.argv) != 2:
    #    sys.exit("Usage: python pagerank.py corpus")
    ff = 'C:/Users/iTTaste/Desktop/CS50Beyond/pagerank/corpus0'
    corpus = crawl(ff)
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

    print('Corpus: ',pages)
    transition_model(pages, '3.html', DAMPING)
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    page_prob_dict = dict()

    page_prob = (1 - damping_factor) / (len(corpus[page]) + 1) 
    prob_links = damping_factor / len(corpus[page]) + page_prob
        
    page_prob_dict[page] = page_prob
    for link in corpus[page]:
        page_prob_dict[link] = prob_links

    return page_prob_dict


def sample_pagerank(corpus, damping_factor, n):
    """ 
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    page = '3.html'
    transition_matrix = transition_model(corpus,page,damping_factor)
    #print('Transition matrix',transition_matrix)
    pages = list(corpus.keys())
    hits = []
    for i in range(n):
        #Make a random move
        r = random.random()
        total = 0.0
        for j in range(0, len(transition_matrix.values())):
            #Find interval containing r
            total += list(transition_matrix.values())[j]
            if total > r:
                page = list(transition_matrix.keys())[j]
                break
        hits.append(page)

    #Write the page ranks
    page_rank = Counter(hits)
    for p in page_rank:
        page_rank[p] = page_rank[p] / len(hits)
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """    
    rank = dict()
    repeat = True
    
    #calculate pages initial rank
    total_pg = total_pages(corpus)
    for page in corpus:
        rank[page] = 1 / len(corpus.keys())

    # calculate the first portion of formula
    first_portion = (1-damping_factor) / total_pg 

    #calculate page rank based on formula
    while repeat is True:
        old_rank = rank.copy()
        for pg in corpus:
            new_rank = first_portion + calc_second_portion(pg, rank, corpus)
            rank[pg] = new_rank 
        for key in rank:
            if key in old_rank:
                if (abs(rank[key] - old_rank[key]) <= 0.001):
                    repeat = False
    return rank

def total_pages(corpus):
    return len(corpus.keys())

def pr(page, corpus):
    relevant_links = []
    for key, links in corpus.items():
        for link in links:    
            if link == page:
                relevant_links.append(key)
    return relevant_links

def num_liks(corpus, page):
    page_degree = len(corpus[page])
    return page_degree

def calc_second_portion(page, rank, corpus):
    #Calculate second portion of the formula
    pr_i = pr(page, corpus)
    sum = 0.0
    for i in pr_i:
        sum += rank[i] / num_liks(corpus,i)
    second_portion = DAMPING * sum
    return second_portion
    
if __name__ == "__main__":
    main()
