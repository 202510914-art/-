#!/usr/bin/env python3
# Affine cipher decrypt/encrypt helper
# Usage:
#   python affine_cipher.py decrypt ENJOY 3 5
#   python affine_cipher.py encrypt RUKDP 3 5
#   or call the functions decrypt_affine(cipher, a, b) / encrypt_affine(plain, a, b)

from typing import Optional, Callable
import sys
import math


def modinv(a: int, m: int) -> Optional[int]:
    # Extended Euclidean algorithm to find modular inverse of a mod m
    a = a % m
    if math.gcd(a, m) != 1:
        return None
    # Extended GCD to compute inverse
    t0, t1 = 0, 1
    r0, r1 = m, a
    while r1:
        q = r0 // r1
        r0, r1, t0, t1 = r1, r0 - q * r1, t1, t0 - q * t1
    inv = t0 % m
    return inv


def _transform_char(c: str, fn: Callable[[int], int]) -> str:
    if 'A' <= c <= 'Z':
        x = ord(c) - ord('A')
        y = fn(x) % 26
        return chr(y + ord('A'))
    if 'a' <= c <= 'z':
        x = ord(c) - ord('a')
        y = fn(x) % 26
        return chr(y + ord('a'))
    return c


def decrypt_affine(cipher: str, a: int, b: int) -> str:
    inv = modinv(a, 26)
    if inv is None:
        raise ValueError(f"a={a} has no modular inverse mod 26 (gcd(a,26) != 1). Choose a coprime with 26.")
    return ''.join(_transform_char(c, lambda x: inv * (x - b)) for c in cipher)


def encrypt_affine(plain: str, a: int, b: int) -> str:
    # For testing / roundtrip
    return ''.join(_transform_char(c, lambda x: a * x + b) for c in plain)


def parse_key(s: str):
    # Accept "3 5", "3,5", "(3,5)"
    s = s.strip()
    s = s.strip('()')
    if ',' in s:
        parts = s.split(',')
    else:
        parts = s.split()
    if len(parts) != 2:
        raise ValueError("키는 a b 또는 a,b 또는 (a,b) 형태로 주십시오.")
    return int(parts[0]), int(parts[1])


def main():
    if len(sys.argv) < 4:
        print("Usage examples:")
        print("  python affine_cipher.py decrypt ENJOY 3 5")
        print("  python affine_cipher.py encrypt RUKDP 3 5")
        print("  python affine_cipher.py decrypt ENJOY \"(3,5)\"")
        return

    mode = sys.argv[1].lower()
    text = sys.argv[2]
    # parse key from next args (either two separate or one like "(3,5)")
    if len(sys.argv) == 5:
        a = int(sys.argv[3])
        b = int(sys.argv[4])
    else:
        a, b = parse_key(sys.argv[3])

    if mode.startswith('d'):
        try:
            out = decrypt_affine(text, a, b)
        except ValueError as e:
            print("Error:", e)
            return
        print(out)
    else:
        print(encrypt_affine(text, a, b))


if __name__ == "__main__":
    main()
