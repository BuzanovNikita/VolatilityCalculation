from scipy.stats import norm
from math import sqrt, exp, log, pi

def d(sigma, P, X, r, t):
    d1 = 1 / (sigma * sqrt(t)) * ( log(P/X) + (r + sigma**2/2) * t)
    d2 = d1 - sigma * sqrt(t)
    return d1, d2

def call_price(sigma, P, X, r, t, d1, d2):
    C = norm.cdf(d1) * P - norm.cdf(d2) * X * exp(-r * t)
    return C

#S  = spot
#K  = strike
#C  = price of call as predicted by Black-Scholes model
#r  = risk-free interest rate
#t  = time to expiration expressed in years
#C0 = price of call option from option chain

P = 100.0
X = 105.0
r = 0.01
t = 30.0/365
C0 = 2.30

#We need a starting guess for the implied volatility.  We chose 0.5
#arbitrarily.
vol = 0.5

epsilon = 1.0  #  Define variable to check stopping conditions
abstol = 1e-4  #  Stop calculation when abs(epsilon) < this number

i = 0   #  Variable to count number of iterations
max_iter = 1e3  #  Max number of iterations before aborting

while epsilon > abstol:
    #if-statement to avoid getting stuck in an infinite loop.
    if i > max_iter:
        break

    i = i + 1
    orig = vol
    d1, d2 = d(vol, P, X, r, t)
    function_value = call_price(vol, P, X, r, t, d1, d2) - C0
    vega = P * norm.pdf(d1) * sqrt(t)
    print ("sigma", i, " = ", vol)
    vol = -function_value/vega + vol
    epsilon = abs(function_value)

print ("Implied volatility = ",  vol)
print ("Code required", i , "iterations.")
