import math

def twoSum(a, b):
    s = a + b
    aEff = s - b  # amount of a in the truncated s
    bEff = s - aEff  # ^ amount of b
    aErr = a - aEff  # a's error
    bErr = b - bEff
    e = aErr + bErr  # total error
    return (s, e)

    

def ddadd(x0, x1, y0, y1):
    (a0, a1) = twoSum(x0, y0)
    (b0, b1) = twoSum(x1, y1)
    (c0, c1) = twoSum(a1, b0)   # c1 is discarded (infinitesimal)
    (d0, d1) = twoSum(a0, c0)
    (e0, e1) = twoSum(d1, b1)   # e1 discarded
    (z0, z1) = twoSum(d0, e0) 
    return (z0, z1)


def madd(x0, x1, y0, y1):
    (a0, a1) = twoSum(x0, y0)
    (b0, b1) = twoSum(x1, y1)
    (c0, c1) = twoSum(a0, b0)
    (d0, d1) = twoSum(a1, b1)   # d1 discarded infinitesimal
    (e0, e1) = twoSum(d0, c1)   # e1 discarded
    (z0, z1) = twoSum(c0, e0)
    return (z0, z1)






# function & test below not actually necessary for actual twoSum computation -- but will keep just if we want to test anything!

    # # Test for both numbers having same number of decimals
    # digits1 = sum(c.isdigit() for c in str(a))
    # digits2 = sum(c.isdigit() for c in str(b))
    # if not digits1 == digits2 or not digits1 == numDigits:
    #     raise ValueError("Incorrect number of digits on one of inputs")

def truncateNDigits(x: float, n: int) -> float:
    """
    Truncate x so that its total number of digits is at most n.
    """
    if x == 0:
        return 0.0
    magnitude = math.floor(math.log10(abs(x)))  # (100->2, 9->0, etc)
    # how much to scale so that truncating leaves n digits
    factor = 10 ** (n - 1 - magnitude)
    # shift, truncate toward zero, then shift back
    return math.trunc(x * factor) / factor