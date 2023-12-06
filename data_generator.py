import random

def generate_data(n):
    W = random.randint(1,500)
    values = [random.randint(1, 100) for _ in range(n)]
    weights = [random.randint(1, 100) for _ in range(n)]
    return values, weights, W

def write_to_file(values, weights, W,filename):
    with open(filename, 'w') as f:
        f.write(f"W: {W} \n")
        f.write(f"Values: {values} \n" )
        f.write(f"Weights: {weights} \n ")


n_small = 100
values, weights,W = generate_data(n_small)
write_to_file(values, weights, W, 'dataset1.txt')

n_medium = 1000
values, weights,W = generate_data(n_medium)
write_to_file(values, weights, W, 'dataset2.txt')

n_large = 10000
values, weights,W = generate_data(n_large)
write_to_file(values, weights, W, 'dataset3.txt')
