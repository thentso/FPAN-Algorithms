import math

# Testing Multiplcation

class DDFloat:
    def __init__(self, x0: float, x1: float):
        self.x0 = x0
        self.x1 = x1
    
    def __pos__(self):
        return DDFloat(self.x0, self.x1)

    def __neg__(self):
        # negates both components
        return DDFloat(-self.x0, -self.x1)

    def __add__(self, rhs):  # representing the ddadd function
        assert isinstance(rhs, DDFloat), f"Second variable is not a DDFloat, got {type(rhs)}"
        z0, z1 = ddadd(self.x0, self.x1, rhs.x0, rhs.x1)
        return DDFloat(z0, z1)
    
    def __sub__(self, rhs):
        return self + (-rhs)
    
    def __mul__(self, rhs):
        assert isinstance(rhs, DDFloat), f"Second variable is not a DDFloat, got {type(rhs)}"
        z0, z1 = ddmul(self.x0, self.x1, rhs.x0, rhs.x1)
        return DDFloat(z0, z1)
    

    def __truediv__(self, rhs):
        assert isinstance(rhs, DDFloat)
        # 1) seed reciprocal as a DD number (low part zero)
        u = DDFloat(1.0 / rhs.x0, 0.0)
        one = DDFloat(1.0, 0.0)

        # 2) one Newton step: u ← u + u*(1 - rhs*u)
        #    all ops now use ddadd/ddmul under the hood
        residual = one - (rhs * u)   # (1 - y*u)
        correction = u * residual    # u*(1 - y*u)
        u = u + correction

        # 3) x / y = x * (1/y)
        return self * u

class MFloat:
    def __init__(self, x0: float, x1: float):
        self.x1 = x1
        self.x0 = x0

    def __pos__(self):
        return MFloat(self.x0, self.x1)

    def __neg__(self):
        # negates both components
        return MFloat(-self.x0, -self.x1)

    def __add__(self, rhs):
        assert isinstance(rhs, MFloat), f"Second variable is not a MFloat, got {type(rhs)}"
        z0, z1 = madd(self.x0, self.x1, rhs.x0, rhs.x1)
        return MFloat(z0, z1)
    
    def __sub__(self, rhs):
        return self + (-rhs)

    def __mul__(self, rhs):
        assert isinstance(rhs, MFloat), f"Second variable is not a MFloat, got {type(rhs)}"
        z0, z1 = mmul(self.x0, self.x1, rhs.x0, rhs.x1)
        return MFloat(z0, z1)
    
    def __truediv__(self, rhs):
        assert isinstance(rhs, MFloat)
        # 1) seed reciprocal as a DD number (low part zero)
        u = MFloat(1.0 / rhs.x0, 0.0)
        one = MFloat(1.0, 0.0)

        # 2) one Newton step: u ← u + u*(1 - rhs*u)
        #    all ops now use ddadd/ddmul under the hood
        residual = one - (rhs * u)   # (1 - y*u)
        correction = u * residual    # u*(1 - y*u)
        u = u + correction

        # 3) x / y = x * (1/y)
        return self * u


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




#  Splits 53-bit IEEE double precision floating point number into a_hi, a_lo, such that a = a_hi + a_lo * a_hi
def split(a): 
    t =(2**27 + 1) * a
    a_hi = t - (t - a)
    a_lo = a - a_hi
    return (a_hi, a_lo)


def twoProd(a, b):
    p = a * b
    (ah, al) = split(a)
    (bh, bl) = split(b)
    e = ((ah * bh - p) + ah * bl + al * bh) + al * bl
    return (p, e)



def ddmul(x0, x1, y0, y1):
    p00, e00 = twoProd(x0, y0)
    p01, e01 = twoProd(x0, y1)
    p10, e10 = twoProd(x1, y0)
    p11, e11 = twoProd(x1, y1)
    t1, t2 = twoSum(p00, p01 + p10)
    return twoSum(t1, t2 + e00 + p11)


def mmul(x0, x1, y0, y1):
    p00, e00 = twoProd(x0, y0)
    p01, e01 = twoProd(x0, y1)
    p10, e10 = twoProd(x1, y0)
    p11, e11 = twoProd(x1, y1)
    temp = p01 + p10
    return twoSum(p00, e00 + temp)





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