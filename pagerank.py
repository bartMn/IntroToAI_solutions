import os
import random
import re
import sys
import numpy as np
import copy

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
    p_dic= dict()
    p1= 1/len(corpus)*(1- damping_factor)
    try:
        p2= 1/len(corpus[page])*damping_factor
    except:
        p1=1/len(corpus)
        p2=0
    for pg in corpus:
        p_dic[pg]= p1
        if pg in corpus[page]:
            p_dic[pg]+= p2
    
    return p_dic


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result={}
    for p in corpus:
        result[p]=0
    new_page= [random.choice(list(corpus))]
 
    for i in range(n):
        options= transition_model(corpus, new_page[0], damping_factor)

        new_page= np.random.choice(
                                list(options),
                                1,
                                p= [options[x] for x in options]
                                )
       
        result[new_page[0]]+=1
        
    for page in result:
        result[page]/=n
        
    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    i_pr= {}
    for p in corpus:
        i_pr[p]= 1/len(corpus)
    
    while True:
        x=0
        temp= copy.copy(i_pr)
        
        for p in i_pr:
            i_pr[p]=(1-damping_factor)/len(i_pr)
            for p1 in i_pr:
                if p in corpus[p1]:
                    i_pr[p]+= damping_factor*temp[p1]/len(corpus[p1])
                elif len(corpus[p1])==0:
                    i_pr[p]+= damping_factor*temp[p1]/len(corpus)
        
        for p in i_pr:
            if abs(i_pr[p]-temp[p])> 0.001:
                x+=1
        if x!=0:
            continue
        return i_pr


if __name__ == "__main__":
    main()
