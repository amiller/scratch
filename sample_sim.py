import numpy as np

def sample_exeriment(k, E, L):
    j = 0

def exp_cdf(e, x): return 1 - np.exp(-x/e)

def efficiency(k=20, L=1.):
    p = 1 - exp_cdf(1, L)
    pk = (1-p)*pow(p,k-1) / (1 - pow(p,k))
    p0 = 1./k
    return pk / p0

def make_graph(k=20):
    global x, y
    x = np.arange(0.001,3,0.01)
    y = [efficiency(k, L/k) for L in x]
    plot(x, y, label=k)

def make_graphs():
    for k in [1,2,3,4,5,10,20]:
        make_graph(k)
    legend()
