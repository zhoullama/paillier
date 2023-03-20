import random
import gmpy2


def getprimeover(n):
    r = gmpy2.mpz(random.SystemRandom().getrandbits(n))
    r = gmpy2.bit_set(r, n-1)
    return int(gmpy2.next_prime(r))


if __name__ == '__main__':
    n_list = [2 ** x for x in range(1, 11)]
    for n in n_list:
        print("n =", n)
        t_min = 2**(n-1)
        for i in range(10):
            t = getprimeover(n)
            print("t =", t)
            assert t_min <= t
