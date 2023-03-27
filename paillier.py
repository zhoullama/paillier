import random
import gmpy2
import gmpy_math


class PaillierKeypair(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_keypair(n_length=1024):
        p = q = n = None
        n_len = 0

        while n_len != n_length:
            p = gmpy_math.getprimeover(n_length // 2)
            q = p
            while q == p:
                q = gmpy_math.getprimeover(n_length // 2)
            n = p * q
            n_len = n.bit_length()

        public_key = (n, n+1)
        private_key = (p, q)

        return public_key, private_key


def paillierEncrypt(plaintext, public_key, random_value=None):
    n = public_key[0]
    g = public_key[1] # g = n+1
    n_square = n * n
    # ciphertext = gmpy2.powmod(g, plaintext, n_square)
    '''"(n+1)^plaintext mod n^2" equals "(n * plaintext + 1) mod n^2".
    This can be simply derived by binomial theorem.
    So we can apply an optimization as follows:
    '''
    ciphertext = (n * plaintext + 1) % n_square
    r = random_value or random.SystemRandom().randrange(1, n)
    assert gmpy2.gcd(r, n) == 1
    obfuscator = gmpy2.powmod(r, n, n_square)
    return (ciphertext * obfuscator) % n_square


def l_func(x, n):
    return gmpy2.mpz((x-1) // n)


def paillierDecrypt(ciphertext, public_key, private_key):
    n = public_key[0]
    g = public_key[1]
    n_square = n * n
    p = private_key[0]
    q = private_key[1]
    lamda = gmpy2.lcm(p-1, q-1)
    c1 = l_func(gmpy2.powmod(ciphertext, lamda, n_square), n)
    g1 = l_func(gmpy2.powmod(g, lamda, n_square), n)
    g1_inv = gmpy2.invert(g1, n)
    return (c1 * g1_inv) % n


if __name__ == '__main__':
    pub, pri = PaillierKeypair.generate_keypair()
    print("n =", pub[0])
    print("g =", pub[1])
    print("p =", pri[0])
    print("q =", pri[1])
    print("n^2 =", pub[0] * pub[0])
    test_num1 = 1234567890
    test_num2 = 9012345678
    m1 = gmpy2.mpz(test_num1)
    m2 = gmpy2.mpz(test_num2)
    print("Plaintext m1:", m1)
    c1 = paillierEncrypt(m1, pub)
    print("Encrypted m1:", c1)
    assert paillierDecrypt(c1, pub, pri) == m1
    print("Plaintext m2:", m2)
    c2 = paillierEncrypt(m2, pub)
    print("Encrypted m2:", c2)
    assert paillierDecrypt(c2, pub, pri) == m2

    c3 = (c1 * c2) % (pub[0] * pub[0])
    m3 = paillierDecrypt(c3, pub, pri)
    print("Decrypted m3:", m3)
    assert m3 == (m1 + m2)

