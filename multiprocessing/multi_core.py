import time
import math
import multiprocessing

# SETTINGS
LIST_SIZE = 10**6 - 1
ITER_COUNT = 10**3
NUM_PROCESSES = 6

def computationally_expensive_function(
        input: list[int | float],
        out_queue: multiprocessing.Queue,
        original_order: int,
        iterations: int = ITER_COUNT,
):
    """
    Computationally expensive process for testing multi core improvement
    """
    print(input[:10])
    out = list(range(len(input)))
    for i, value in enumerate(input):
        out[i] = value
        if i % 1000 == 0:
            print(f"Process {original_order} on list item #: {i}")
        for _ in range(iterations):
            out[i] = (out[i] + 1) / 1.00001
    print("end of compute")
    out_queue.put((original_order, out))
    print(f"finished thread {original_order}")
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
    # Split data into 4 lists
    chunksize = math.ceil(len(test) / NUM_PROCESSES)
    chunklist = []
    out_queue = multiprocessing.Queue()
    processlist = [None] * NUM_PROCESSES
    chunk_len_check = 0
    for i in range(NUM_PROCESSES):
        print(f"CHUNK #: {i}")
        if i + 1 < NUM_PROCESSES:
            chunklist.append(test[i*chunksize: (i + 1)*chunksize])
        else:
            chunklist.append(test[i*chunksize:])
        
        print(len(chunklist[i]))

        processlist[i] = multiprocessing.Process(
            target=computationally_expensive_function, 
            args=(chunklist[i], out_queue, i))

        chunk_len_check += len(chunklist[i])

    # Verify the length of all the chunks adds up to original list to make sure nothing 
    # is being left off.
    assert chunk_len_check == len(test)

    for i in range(NUM_PROCESSES):
        processlist[i].start()


    # Retrive items from queue and put into outlist
    # Need to reorder to put list back together in original format
    # Processes will also not terminate in join until their output 
    # has been returned by queue according to: 
    # https://stackoverflow.com/questions/50483576/multiprocessing-process-doesnt-terminate-after-putting-requests-response-conten
    counter = 0
    outlist = [None] * NUM_PROCESSES
    while counter < NUM_PROCESSES:
        i, out = out_queue.get()
        outlist[i] = out
        time.sleep(1) # check every 1 second
        counter += 1

    for i in range(NUM_PROCESSES):
        print(f"joining process {i}")
        processlist[i].join()

    out = []
    for out_i in outlist:
        out += out_i

    print("reached tok")
    tok = time.perf_counter()

    print("\n\n----------")
    print("Preview of output: ")
    print(f"Length of output {len(out)}")
    print("First ten items in output list: ")
    print(out[:10])
    print("\nLast ten items in output list: ")
    print(out[-10:])

    print("\n\n----------")
    print(f"\nTotal Runtime (secs): {round(tok - tik, 2)}")

    return out


if __name__ == "__main__":
    main_process()
