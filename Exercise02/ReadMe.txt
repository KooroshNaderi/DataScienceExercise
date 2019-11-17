Problem: using multi-processing to find a regular expression matching part of a big data

Solution: The MatchingURLs.ipynb contains the solution
- I did not have a big data on urls, so a simple problem is solved
- Multi-processing is used on each regular expression given the dataset to find the matching
- A queue and dictionary are used to return the results
- In case of having million or more dataset of urls, a contious loop would make sense to be used,
  and gradually collect the answers

To run: you need Jupyter notebook for running the solution.