

# f:       file size
# d >= 1:  ratio of total peer storage to file size
# B >= 1:  number of blocks in the original file
# r >= 1:  erasure encoding rate

# total encoded file size: r*f
# number of blocks drawn in a round: d*B
# p1: probability of a particular subset not being included:  ((r-1)/r)**(d*B)
# union bound: (rB choose B) * p1

# Stirling approximation of (rB choose B):  r**(r*(B-1)+1) / (r-1)**((r-1)*(B-1))

# overall approximation: (r**-0.5) * (r/(r-1))**(r*(B-1) - d*B) * r / (r-1)**(1-B)

# r**(Br-r+1) / (r-1)**((Br-r-B+1)
# (r/(r-1))**(r*(B-1)-d*B) * r / (r-1)**(1-B)

import numpy as np
from pylab import *

def pr_approx(r, B, d): 
    r = float(r)
    B = float(B)
    d = float(d)
    assert r >= 2 and B >= 1 and d >= 1
    return (B**-0.5) * (r/(r-1))**(r*(B-1) - d*B) * r / (r-1)**(1-B)

def pr_special(r, B, d): 
    import scipy.special
    r = float(r)
    B = float(B)
    d = float(d)
    assert r >= 2 and B >= 1 and d >= 1
    return scipy.special.binom(r*B,B) * ((r-1)/r)**(d*B)


def graphs():
    Bs = arange(1, 40, 1)
    rs = arange(2, 3, 0.2)
    ds = arange(1, 5)
    for i,d in enumerate(ds):
        figure(i)
        clf()
        for r in rs:
            plot(Bs, [pr_special(r, B, d) for B in Bs])
        title('Pr[failure] vs block subdivisions (d = %.2f), encoding rate r' % d)
        xlabel('B (# of blocks)')
        ylabel('Pr[failure]')
        ylim([0,1])
        legend(['r = %.2f' % r for r in rs])
                      
