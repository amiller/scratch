import numpy as np

def sample_exeriment(k, E, L):
    j = 0

def exp_cdf(e, x): return 1 - np.exp(-x/e)

def efficiency(k=20, L=1., E=1.):
    p = 1 - exp_cdf(E, L)
    pk = (1-p)*pow(p,k-1) / (1 - pow(p,k))
    p0 = 1./k
    return pk / p0 * p

def make_graph(k=20):
    global x, y
    x = np.arange(0.001,3,0.01)
    y = [efficiency(k, L/k) for L in x]
    plot(x, y, label=k)

def make_graphs():
    for k in [1,2,3,4,5,10,20,1000]:
        make_graph(k)
    legend()

def ideal_cloud_cost(E, k, b):
    # Cost ($) per byte of bandwidth 
    #cost_per_byte = 0.12 / (1024*1024*1024) # 12 cents / GB  # Amazon EC2
    # .14 cents / GB  # Amortized, bulk $7/mbps
    cost_per_mbps = 1.00 # $1/mbps
    seconds_per_month = 2.62974e6
    cost_per_byte = cost_per_mbps / seconds_per_month / 1e6 * 8 
    # Round trip latency (seconds)
    latency = 0.030 # 30 ms, UMD to EC2 US.East
    L = latency
    if k == 1: print 'Ideal cloud cost per iter:',  (b * cost_per_byte)
    #cost = (1./efficiency(k, L, E)) * (k * 15 * cost_per_byte) # 15: cost for a single hash
    cost = (1./efficiency(k, L, E)) * (k * b * cost_per_byte)
    #print efficiency(k,L,E)
    return cost

def ssd_local_cost_sub4096(E, k, b):
    assert b <= 4096, "This SSD model holds only for reads <= 4096 bytes"
    # Cost ($) per second
    cost_per_sec = 1.03e-7 + 1.056e-5 # Power + laptop and SSD over 3 yrs
    # Total latency per read/sign iteration (seconds)
    latency = 6.0 / (10000 * 20)
    cost_per_iter = latency * cost_per_sec
    if k == 1: print 'Local SSD cost per iter:',  cost_per_iter
    L = latency
    #print efficiency(k,L,E)
    cost = (1./efficiency(k, L, E)) * (k * cost_per_iter)
    return cost
    
def graph1():
    x = np.arange(1,80000)
    E = 600 # 10 minutes
    b = 4096
    y1 = [ideal_cloud_cost(E, k, b) for k in x]
    y2 = [ssd_local_cost_sub4096(E, k, b) for k in x]
    clf()
    plot(x, y1, label='Ideal Cloud')
    plot(x, y2, label='SSD Sequential')
    legend()
    title('Effective cost per ticket vs iterations')
    xlabel('k (puzzle iterations)')
    ylabel('Effectve cost per ticket ($)')
