Mar 2025  
Author: Spencer Vore  


# Summary
This repository is my recreation (mostly) from memory of the multi-threaded and multi-core examples show in the Concurrent and Parallel Programming in Python course: 
https://www.udemy.com/course/concurrent-and-parallel-programming-in-python/  
Also, the final code from this course is here:
https://github.com/codingwithmax/threading-tutorial/tree/main 

I wanted to get some hands on experience with some of the basic Python multithreading and parallel libraries.  

NOTE: The code in this example is solely inspired by the Udemy training course and doesn't contain any confidential information or anything work related.  


# Repository Contents / File Descriptions:
- multiprocessing directory - Contains multi-core example
    - single_core.py - Single core (single thread) version of a simple compute heavy program. This file was then copied to make the multi-core version.
    - multi_core.py - Multicore version using multiprocessing.Process()
    - multi_core_w_pool - Simplified example of multi_core using Pool(). Way less code, and even better runtime performance!
    - compare_outputs.py - Runs the single core, then the multi core versions. Compare all the final results to prove they're exactly the same. Shows that the multicore versions aren't changing the computation.
    - multiprocess_runtimes.txt - Recorded the final runtime to compare the three scripts to show performance improvement.

- threading_w_asyncio - An example of a stock price web scraper (scrapes prices from google finance). This shows how to multi-thread it using asyncio and aiohttp
    - single_threaded_async.py - Single threaded version of the stock price web scraper. This file was then copied to create the multi-thread version.
    - multi_threaded_async - Multi threaded version using aiohttp and asyncio. Async processes are launched using asyncio.create_task().

- threading_w_threading_lib - A lower level implementation example of a multi-threaded program using Python's threading.Thread(). We can multi-thread functions not designed to use asyncio with this method, so it's more general to all of Python. These threads will appear in the Operating System Activity Monitor, as it uses the operating system to manage the threads (not the Python interpreter as with asyncio).
    - single_threaded - Basic single threaded version of stock price web scraper. Used the yFinance Python library to retrieve stock prices from Yahoo Finance. The current (Mar 2025) Yahoo website seems to be designed to block my direct attempts to scrape it using Python's requests library, so I wasn't able to convert this to aiohttp to try and multithread it using async. That's why I build a new version of this which scraped stock prices from Google (for threading_w_asyncio example in other directory). This file was then copied to create the multi-thread version.
    - multi_threaded - Multi-threaded implementation. Can run yFinance in multiple threads to speed up results.
    - bad_async_multithread_implementation - Just for fun, I decided to try and multithread the process using asyncio anyways, just to prove it wouldn't work. I was right.
    - threading_runtimes.txt - Recorded the final runtime to compare the two scripts to show performance improvement.
- requirements.txt - Use to build Python to run this code using pip
- .gitignore - Files that git will ignore.


# Setup
This code was run using Python 3.12. Then pip install -r requirements.txt.  

Code was formatted using Python black: `black .`  

