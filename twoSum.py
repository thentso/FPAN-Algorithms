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


TEST_CASES = [
    (8.834235326183948e71,  9.578097123275567e53,
     -4.6316785776358486e77, -2.55523157298961e61,
     -4.6316697434005227e77, -2.037703193040189e60,
     -4.6316697434005227e77, -2.0377031930401882e60),

    (1.4919697328456323e87, 5.521397077432451e70,
     4.973223565419703e86, -4.909094196809657e-91,
     1.9892920893876027e87, -4.909094196809657e-91,
     1.9892920893876027e87,  0.0),

    (-8191.992462158203,     9.143899130258214e-100,
     -9.14613152750686e-100, 2.242825269339505e-117,
     -8191.992462158203,    -2.2323972486468995e-103,
     -8191.992462158203,    -2.232397248646922e-103),

    (-6.344854596578372e-117, 3.5220749571797036e-133,
     4.417117661946964e71,   6.502419267294956e-117,
     4.417117661946964e71,    1.5756467071658512e-118,
     4.417117661946964e71,    1.5756467071658477e-118),

    (-1.6110451730902522e60,  1.3071815033235768e39,
     -2.1567956686498734e68,  1.1972619985767064e52,
     -2.156795684760325e68,  -4.863878519471706e51,
     -2.156795684760325e68,  -4.8638785194717065e51),

    (8.84443087277937e-75,   -2.4072299075463057e-91,
     1.7413332937543717e45, -8.843436600161344e-75,
     1.7413332937543717e45,   9.942726180261331e-79,
     1.7413332937543717e45,   9.942726180263738e-79),
]

if __name__ == "__main__":
    for i, (x0, x1, y0, y1, dd0_exp, dd1_exp, m0_exp, m1_exp) in enumerate(TEST_CASES, 1):   # syntax starts i at 1, but still is using each case and forgetting the 0th
        dd0_act, dd1_act = ddadd(x0, x1, y0, y1)
        m0_act,  m1_act  = madd(x0, x1, y0, y1)

        print(f"\n=== Case #{i} ===")
        print(" Inputs: x0=", x0, " x1=", x1, " y0=", y0, " y1=", y1)
        print(" ddadd → actual:   ", (dd0_act, dd1_act))
        print("        expected: ", (dd0_exp, dd1_exp))
        print(" match? ", (dd0_act, dd1_act) == (dd0_exp, dd1_exp))

        print(" madd  → actual:   ", (m0_act, m1_act))
        print("        expected: ", (m0_exp, m1_exp))
        print(" match? ", (m0_act, m1_act) == (m0_exp, m1_exp))