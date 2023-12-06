def unboundedKnapsack(W, n, val, wt): 
  
    # dp[i] is going to store maximum  
    # value with knapsack capacity i. 
    dp = [0 for i in range(W + 1)] 
  
    ans = 0
  
    # Fill dp[] using above recursive formula 
    for i in range(W + 1): 
        for j in range(n): 
            if (wt[j] <= i): 
                dp[i] = max(dp[i], dp[i - wt[j]] + val[j]) 
    
    return dp[W] 

# Contoh input
W = 8
val = [13,8,9,13,12]
wt = [4,2,6,8,5]
n = len(val)
print(unboundedKnapsack(W,n,val,wt))