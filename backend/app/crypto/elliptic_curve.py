from typing import NamedTuple, Optional
import secrets
import hashlib

class Point(NamedTuple):
    x: int
    y: int

    def __eq__(self, other: 'Point'):
        return self.x == other.x and self.y == other.y

class Signature(NamedTuple):
    r: int
    s: int

# -------------------------
# Elliptic Curve Parameters
# -------------------------
# y² = x³ + ax + b
a = 0
b = 7

# prime field
p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1

# number of points on the curve we can hit ("order")
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

# generator point (the starting point on the curve used for all calculations)
G = Point(
    55066263022277343669578718895168534326250603453777594175500187360389116729240,
    32670510020758816978083085130507043184471273380659243275938904335757337482424
)

def inverse(a, m = p) -> Point:
    m_orig = m
    if a < 0:
        a = a % m

    prevy, y = 0, 1
    while a > 1:
        q = m // a
        y, prevy = prevy - q * y, y
        a, m = m % a, a
    return y % m_orig

def double(point: Point) -> Point:
    # slope = (3x₁² + a) / 2y₁
    slope = ((3 * point.x ** 2 + a) * inverse((2 * point.y), p)) % p # using inverse to help with division

    # x = slope² - 2x₁
    x = (slope ** 2 - (2 * point.x)) % p

    # y = slope * (x₁ - x) - y₁
    y = (slope * (point.x - x) - point.y) % p

    return Point(x,y)

def add(point1: Point, point2: Point) -> Point:
    # double if both points are the same
    if point1 == point2:
        return double(point1)

    # slope = (y₁ - y₂) / (x₁ - x₂)
    slope = ((point1.y - point2.y) * inverse(point1.x - point2.x, p)) % p

    # x = slope² - x₁ - x₂
    x = (slope ** 2 - point1.x - point2.x) % p

    # y = slope * (x₁ - x) - y₁
    y = ((slope * (point1.x - x)) - point1.y) % p

    # Return the new point
    return Point(x,y)

# --------
# Multiply: use double and add operations to quickly multiply a point by an integer value (i.e. a private key)
# --------
def multiply(k: int, point: Optional[Point] = None) -> Point:
    if point is None:
        point = Point(G.x, G.y)
    # create a copy the initial starting point (for use in addition later on)
    current = Point(point.x, point.y)

    # convert to binary string and remove '0b' prefix
    binary = bin(k)[2:]

    # double and add algorithm for fast multiplication
    for char in binary[1:]:
        current = double(current)
        if char == '1':
            current = add(current, point)
    return current

# ----
# Sign
# ----
def sign(private_key: int, hash_digest: int, nonce: Optional[int]=None) -> Signature:
    # generate random number if not given
    if nonce is None:
        while True:
            nonce = secrets.randbits(256)
            if nonce < n: # make sure random numer is below the number of points of the curve
                break

    # r = the x value of a random point on the curve
    r = multiply(nonce).x % n

    # s = nonce⁻¹ * (hash_string + private_key * r) mod n
    s = (inverse(nonce, n) * (hash_digest + private_key * r)) % n # this breaks linearity (compared to schnorr)

    # signature is {'r': r, 's': s}
    return Signature(r,s)

# ------
# Verify
# ------
def verify(public_key: str, signature: Signature, hash_digest: int):
    public_key_point = Point(int(public_key[2:2+64], 16), int(public_key[2+64:2+64*2], 16))

    # point 1
    point1 = multiply(inverse(signature.s, n) * hash_digest)

    # point 2
    point2 = multiply((inverse(signature.s, n) * signature.r), public_key_point)

    # add two points together
    point3 = add(point1, point2)

    # check x coordinate of this point matches the x-coordinate of the random point given
    return point3.x == signature.r

private_key = "f94a840f1e1a901843a75dd07ffcc5c84478dc4f987797474c9393ac53ab55e6"

# Public key is the generator point multiplied by the private key
point = multiply(int(private_key, 16))

# convert x and y values of the public key point to hexadecimal
x = hex(point.x)[2:].rjust(64, "0") # pad with zeros to make sure it's 64 characters (32 bytes)
y = hex(point.y)[2:].rjust(64, "0")

# uncompressed public key (use full x and y coordinates) OLD FORMAT!
public_key_uncompressed = "04" + x + y

print(public_key_uncompressed)

msg = "Hello World!"
hash_digest = int(hashlib.sha256(msg.encode()).hexdigest(), 16)

signature = sign(int(private_key, 16), hash_digest, 12345678)

# should be true
print(verify(public_key_uncompressed, signature, hash_digest))

wrong_public_key_uncompressed = "04" + y + y

# should be false
print(verify(wrong_public_key_uncompressed, signature, hash_digest))
