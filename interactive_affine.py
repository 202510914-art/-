#!/usr/bin/env python3
# Interactive Affine cipher tool
# 실행: python interactive_affine.py
# 동작: 암호화(encrypt) 또는 복호화(decrypt)를 선택하고,
#       텍스트와 키 (a,b)를 입력하면 결과를 출력합니다.
# 예:
#  mode: decrypt
#  text: ENJOY
#  key: (3,5)
#  출력: RUKDP

from typing import Optional, Callable
import math
import sys


def modinv(a: int, m: int) -> Optional[int]:
    a = a % m
    if math.gcd(a, m) != 1:
        return None
    t0, t1 = 0, 1
    r0, r1 = m, a
    while r1:
        q = r0 // r1
        r0, r1, t0, t1 = r1, r0 - q * r1, t1, t0 - q * t1
    return t0 % m


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
        raise ValueError(f"a={a}는 26과 서로소가 아니어서 역수가 존재하지 않습니다.")
    return ''.join(_transform_char(c, lambda x: inv * (x - b)) for c in cipher)


def encrypt_affine(plain: str, a: int, b: int) -> str:
    return ''.join(_transform_char(c, lambda x: a * x + b) for c in plain)


def parse_key_input(s: str):
    s = s.strip()
    if s.lower() in ('q','quit','exit'):
        return None
    s = s.strip('()')
    if ',' in s:
        parts = [p.strip() for p in s.split(',')]
    else:
        parts = s.split()
    if len(parts) != 2:
        raise ValueError("키는 a b 또는 a,b 또는 (a,b) 형태로 입력하세요.")
    return int(parts[0]), int(parts[1])


def prompt(prompt_text: str) -> str:
    try:
        return input(prompt_text)
    except (EOFError, KeyboardInterrupt):
        print()
        return 'q'


def main():
    print("Interactive Affine Cipher")
    print("종료하려면 mode나 text나 key에 q 또는 quit 입력")
    while True:
        mode = prompt("mode (encrypt/decrypt) > ").strip().lower()
        if mode in ('q','quit','exit'):
            break
        if not (mode.startswith('e') or mode.startswith('d')):
            print("encrypt 또는 decrypt 중 하나를 입력하세요.")
            continue

        text = prompt("text > ")
        if text.strip().lower() in ('q','quit','exit'):
            break

        key_in = prompt("key (a b) or (a,b) > ")
        if key_in.strip().lower() in ('q','quit','exit'):
            break

        try:
            key = parse_key_input(key_in)
            if key is None:
                break
            a, b = key
        except Exception as e:
            print("키 입력 오류:", e)
            continue

        if math.gcd(a, 26) != 1:
            print(f"경고: a={a} 는 26과 서로소가 아닙니다. 가능한 a 값: 1,3,5,7,9,11,15,17,19,21,23,25")
            continue

        try:
            if mode.startswith('d'):
                out = decrypt_affine(text, a, b)
                print("decrypted >", out)
            else:
                out = encrypt_affine(text, a, b)
                print("encrypted >", out)
        except Exception as e:
            print("오류:", e)

    print("종료합니다.")


if __name__ == "__main__":
    main()
