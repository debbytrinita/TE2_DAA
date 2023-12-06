from memory_profiler import memory_usage
import time
from unbounded_knapsack_dp import unboundedKnapsack
from knapsack_branch_and_bound import knapsack_branch_and_bound


def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        W_line = lines[0].strip().split(':')[1].strip()
        val_line = lines[1].strip().split(':')[1].strip()
        wt_line = lines[2].strip().split(':')[1].strip()

        W = int(W_line)
        val = list(map(int, val_line[1:-1].split(',')))
        wt = list(map(int, wt_line[1:-1].split(',')))
        n = len(val)
        return W, val, wt, n

for i in range(3):

    memory_before = memory_usage()[0]
    W, val, wt,n = read_file(f"dataset{i+1}.txt")
    start_time = time.time()
    z_hat,x_hat = knapsack_branch_and_bound(W,val,wt)
    end_time = time.time()
    elapsed_time = end_time-start_time
    memory_after = memory_usage()[0]
    total_memory_usage = memory_after-memory_before

    print(f"Branch and Bound: dataset{i+1}.txt")
    print(f'Best Solution: {z_hat}')
    print(f"Elapsed time : {elapsed_time}")
    print(f"Total memory usage : {total_memory_usage}")
    print()

for i in range(3):

    memory_before = memory_usage()[0]
    W, val, wt,n = read_file(f"dataset{i+1}.txt")
    start_time = time.time()
    z_hat= unboundedKnapsack(W,n,val,wt)
    end_time = time.time()
    elapsed_time = end_time-start_time
    memory_after = memory_usage()[0]
    total_memory_usage = memory_after-memory_before

    print(f"Dynamic Programming: dataset{i+1}.txt")
    print(f'Best Solution: {z_hat}')
    print(f"Elapsed time : {elapsed_time}")
    print(f"Total memory usage : {total_memory_usage}")
    print()

