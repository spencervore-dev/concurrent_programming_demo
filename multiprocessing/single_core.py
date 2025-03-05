# Single core (also single thread) version of a silly computationally expensive process.

import time

# SETTINGS
LIST_SIZE = 10**6 - 1
ITER_COUNT = 10**3


def computationally_expensive_function(
    input: list[int | float], iterations: int = ITER_COUNT
):
    """
    Computationally expensive process for testing multi core improvement
    """

    out = list(range(len(input)))
    for i, value in enumerate(input):
        out[i] = value
        if i % 1000 == 0:
            print(f"On list item #: {i}")
        for _ in range(iterations):
            out[i] = (out[i] + 1) / 1.00001
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
    out = computationally_expensive_function(test)
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
