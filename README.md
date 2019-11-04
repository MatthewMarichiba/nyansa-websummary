# Programming Exercise: Web Analytics
The problem statement is defined here: https://sites.google.com/a/nyansa.com/nyansa-programming-exercise/

## Running my solution
My solution is a Python script called `tally_sites.py`. You will need Python3 installed to run the script. The script uses no 3rd party packages, so it is not necessary to install any custom Python packages. 

To run:

1. `cd` to the root of this repo.
2. `python3 ./tally_sites.py input.txt`

## Notes
Edge cases handled by my solution:

* Basic command-line usage: What if no filename argument, or wrong number of arguments?
* Graceful handling if input line formatting is bad
* Years out of order - Sort dates correctly, even if timestamps span multiple years and are out-of-order


## Big-O Analysis

### Computational Analysis
Let N represent the number of input lines in the input data file. For calculating computational complexity, the constituent terms are:
* Reading the file: O(N)
* Sort dates: Low cardinality of unique dates means this term will be negligent, which we can practically approximate as a constant/negligible O(1).
* Iterate over the following terms for each unique date:
  * Sort URLs by hit-count: **I used Python's built-in `sorted()` function which uses Timsort, an optimized version of merge-sort with worst-case performance of O(N log N)**
  * Print line for each URL on that date: O(N)

If we approximate the cardinality of dates as a constant, c, then the overall Big-O notation is:

* O(N) + c(O(N log N) + O(N))
* Equivalent to: O(N) + O(N log N) + O(N)
* **The dominant term is O(N log N).**

We can expect that the typical case will perform better than the worst case. The `N` in the dominant O(N log N) term represents the cardinality of unique URLs for a day (ie, *not* the number of lines in the file). The cardinality of URLs likey grows slower than the number of lines in the file. Furthermore, Python's `sorted()` Timsort algorithm takes advantage of naturally pre-sorted sequences, which improves the **log(N)** factor. We're sorting on unique hit-count values, which we know to have low cardinality. Therefore, there is a greater-than-random chance that many pre-sorted sequences will exist (Ex: `[1, 1, 1, 1, 3, 3, 4, 6]`), improving performance.

### Memory Analysis
In terms of space complexity, Python's Timsort may need to allocate up to N/2 pointers, where `N` represents the number of unique URLs for a given day. This equates to space complexity of **O(N)**. Given that we have enough memory to hold the entire list of unique URLs, we presumably have enough space to hold N/2 pointers. 
