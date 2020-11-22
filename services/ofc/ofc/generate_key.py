#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import math
import random
import secrets


def is_prime(n):  
    prime_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    for prime in prime_list:
        if n % prime == 0:
            return False

    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    
    for _ in range(128):
        a = random.randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    
    return True


def generate_prime_number(length=1024):
    found_prime = False
    
    while not found_prime:
        p = secrets.randbits(length)
        p |= (1 << length - 1) | 1
        
        found_prime = is_prime(p)
    
    return p


def generate_coprime_number(p):
    p1 = 2
    p2 = (p - 1) // p1

    while True:
        g = random.randint(2, p - 1)
        if pow(g, p1, p) != 1 and pow(g, p2, p) != 1:
            return g



def generate_gost():
    p = generate_prime_number()
    base = generate_coprime_number(p)
    while True:
        a = random.randint(2, p - 2)
        if math.gcd(a, p - 1) == 1:
            break
    b = pow(base, a, p)

    return (p, base, a, b)


def main():
    print(*generate_gost(), sep='\n')


if __name__ == '__main__':
    main()
