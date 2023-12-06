import math
import time
import tracemalloc


def knapsack_branch_and_bound(W,val,wt):
    items = list(zip(val, wt))
    items_eliminated = eliminate_dominated_element(items)
    # sort items based on ratio
    items_eliminated.sort(key=lambda i: i[0] / i[1], reverse=True)

    #initiation
    M = [[0 for _ in range(8)] for _ in range(len(items_eliminated))] 
    x_hat = [0]*len(items_eliminated)
    x = [0]*len(items_eliminated)
    z_hat = 0
    i=0
    w1= items_eliminated[0][1]
    v1=items_eliminated[0][0]
    x[0] = W//w1
    V_N = v1 * x[0]
    W0 = W - (w1 * x[0])
    U = calculate_upper_bound(items_eliminated,V_N,W0,i)
    m = find_mi(items_eliminated)
    
    step = 2

    while True:
        #  Develop
        if step == 2:
            M, items, x, i, V_N, W0, z_hat, x_hat,step = develop(m, W0,z_hat,V_N,x_hat,x,U,i,items,M,W)

        # Backtrack
        elif step == 3:
            M, items, x, i, V_N, W0, z_hat, x_hat,step = backtrack(i,items,z_hat,V_N, W0,m,x_hat,U,x,M)

        # Replace
        elif step == 4:
            M, items, x, i, V_N, W0, z_hat, x_hat,step = replace(i,z_hat,V_N,W0,items,x_hat,x,U,M,m)

        # Finisih
        else:
            break

    return z_hat,x_hat

#  Eliminating the dominated items
def eliminate_dominated_element(items):
    N = list(range(len(items)))
    j = 0
    while j < len(N) - 1:
        k = j + 1
        while k < len(N):
            if ((items[N[k]][1] // items[N[j]][1]) * items[N[j]][0] >= items[N[k]][0]):
                    N.pop(k)
            elif ((items[N[j]][1] // items[N[k]][1]) * items[N[k]][0] >= items[N[j]][0]):
                    N.pop(j)
                    k = len(items)
            else:
                k += 1
        j += 1
        
    items = [items[i] for i in N]
    return items

# calculate UpperBound
def calculate_upper_bound(items,V_N,W0,i):
    if i + 2 >= len(items):
        return V_N
    
    v1, w1 = items[i]
    v2, w2 = items[i + 1]
    v3, w3 = items[i + 2]
    z_1 = V_N + math.floor(W0 / w2) * v2
    W_2 = W0 - math.floor(W0 / w2) * w2
    U_1 = z_1 + math.floor(W_2 * v3 / w3)
    U_2 = z_1 + math.floor(((W_2 + math.ceil((1 / w1) * (w2 - W_2)) * w1)* v2 / w2) - math.ceil((1 / w1) * (w2 - W_2)) * v1)
    U = max(U_1, U_2)
    return U

# Find mi= min{wj: j>i} for all i = 1, 2, ... , n0
def find_mi(items):
    m = [0]*len(items)
    m[-1]= float('inf')
    for i in range(len(items)-2, -1, -1):
        m[i] = min(items[i+1][1], m[i+1])
    return m 

# Find min j such that j>i and wj<=W0
def find_min_j(items, W0, i):
    min_j = []
    for j in range(i + 1, len(items)):
        if items[j][1] <= W0 and j>i:
            min_j.append(j)
    if len(min_j) == 0:
        return -1
    return min(min_j)

# Find max j such that j<=i and x[j]>0
def find_max_j(x, i):
    max_j = []
    for j in range(i + 1):
        if x[j] > 0 and j<=i:
            max_j.append(j)
    if len(max_j) == 0:
        return -1
    return max(max_j)

def develop(m, W0,z_hat,V_N,x_hat,x,U,i,items,M,W):
    if W0 < m[i]:
        if z_hat<V_N:
            z_hat=V_N
            x_hat=x
            if z_hat == U:
                return M, items, x, i, V_N, W0, z_hat, x_hat,5
        return M, items, x, i, V_N, W0, z_hat, x_hat,3 
    else:
        j = find_min_j(items,W0,i)
        if V_N + calculate_upper_bound(items[j],V_N,W0,i) <=z_hat:
            return M, items, x, i, V_N, W0, z_hat, x_hat,3
        if M[i][W0] >= V_N:
            return M, items, x, i, V_N, W0, z_hat, x_hat,3
        x[j] = W0//items[j][1]
        V_N = V_N+ (items[j][0]*x[j])
        W0 = W0 - (items[j][1]* x[j])
        M[i][W0] = V_N
        i = j
        return M, items, x, i, V_N, W0, z_hat, x_hat,2

def backtrack(i,items,z_hat,V_N, W0,m,x_hat,U,x,M):
    j = find_max_j(x,i)
    if j < 1:
        return M, items, x, i, V_N, W0, z_hat, x_hat,5

    i = j
    x[i] = x[i]-1
    V_N = V_N - items[i][0]
    W0 = W0 +  items[i][1]
    if W0 < m[i]:
        return M, items, x, i, V_N, W0, z_hat, x_hat,3
    if V_N + W0 * (items[i+1][0]//items[i+1][1]) <= z_hat:
        V_N = V_N - (items[i][0]*x[i])
        W0 = W0 + (items[i][1]*x[i])
        x[i] = 0
        return M, items, x, i, V_N, W0, z_hat, x_hat,3
    
    if W0 - items[i][1] >= m[i]:
        return M, items, x, i, V_N, W0, z_hat, x_hat,2

def replace(i,z_hat,V_N,W0,items,x_hat,x,U,M,m):
    j = i 
    h = j+1
    if z_hat >=V_N + W0 * (items[h][0]//items[h][1]):
        return M, items, x, i, V_N, W0, z_hat, x_hat,3
    if items[h][1] >= items[j][1]:
        if (items[h][1] == items[j][1]) or (items[h][1]>W0) or (z_hat >= V_N+ items[h][0]):
            h= h+1
            return M, items, x, i, V_N, W0, z_hat, x_hat,4 
        z_hat = V_N + items[h][0]
        x_hat = x
        x[h] = 1
        if z_hat == U:
            return M, items, x, i, V_N, W0, z_hat, x_hat,5
        j = h 
        h = h+1
        return M, items, x, i, V_N, W0, z_hat, x_hat,4
    else:
        if W0 - items[h][1] < m[h-1]:
            h = h+1
            return M, items, x, i, V_N, W0, z_hat, x_hat,4
        i = h 
        x[i] = W0//items[i][1]
        V_N = V_N + items[i][0] * x[i]
        W0 = W0- items[i][1]*x[i]
        return M, items, x, i, V_N, W0, z_hat, x_hat,2

# Contoh input
W = 8
val = [13,8,9,13,12]
wt = [4,2,6,8,5]
z_hat,x_hat =knapsack_branch_and_bound(W,val,wt) 
print(f"Best Value: {z_hat}")



