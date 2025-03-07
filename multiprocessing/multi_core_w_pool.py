# Copy of multi_core.py. Multiprocess / multicore implementation of the same silly
# computationally expensive function to demonstrate benefit of multicore processing.
# We simplified the multi_core implementation greatly by using a Pool. We also got additional performance
# improvement, as the multicore processing is distributed one list element at a time vs. breaking the list into
# 6 lists and distributing them to processes.

import time
from multiprocessing import Pool, cpu_count

# SETTINGS
LIST_SIZE = 10**6 - 1
ITER_COUNT = 10**3
NUM_PROCESSES = 6


def computationally_expensive_function(
    input: int | float, iterations: int = ITER_COUNT
):
    """
    Computationally expensive process for testing multi core improvement
    """
    out = input
    for _ in range(iterations):
        out = (out + 1) / 1.00001
    return out


def main_process():
    """
    Main function to run process
    """
    test = list(range(LIST_SIZE))
    print("Preview of input: ")
    print(f"Length of input: {len(test)}")
    print("First 10 items in input list: ")
    print(test[:10])
    print("\n\n")

    tik = time.perf_counter()

    cpus_to_use = max(1, cpu_count() - 2)
    print(f"CPU's to use: {cpus_to_use}")

    with Pool(cpus_to_use) as pool:
        out = pool.map(computationally_expensive_function, test)

    tok = time.perf_counter()

    print("\n\n----------")
    print("Preview of output: ")
    print(f"Length of output {len(out)}")
    print("First ten items in output list: ")
    print(out[:10])
    print("\nLast ten items in output list: ")
    print(out[-10:])

    print("\n\n----------")
    print(f"TOTAL RUNTIME (secs): {round(tok-tik, 2)}")

    return out


if __name__ == "__main__":
    main_process()
