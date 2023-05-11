import math
import random
import matplotlib.pyplot as plt

# xs=[]

def expRand(λ):
    """
    cdf eqn: R = 1-e^(-λX)
    since R is the ammount of the repeation of X
    then by getting the inverse of the function
    we can get the value of X R number of times
    so the X can be get by getting random R from a uniform distribution 
    """

    r = random.random()
    
    ans = (-1/λ)*math.log(1-r)
    ans = math.ceil(ans) # to scale the points
    
    
    # xs.append(ans) # to show histogram
    
    return ans

# # get 1000 random number
# for i in range(1000):
#     expRand(1/35)

# # showing histogram
# plt.hist(xs,100)
# plt.show()
# print(sorted(xs))

# # reference
# # https://www.eg.bucknell.edu/~xmeng/Course/CS6337/Note/master/node50.html
