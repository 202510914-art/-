# Affine Cipher Helper

이 저장소는 아핀 암호를 쉽게 복호화/암호화할 수 있는 Python 스크립트를 제공합니다.

예:
- 입력: `ENJOY`, 키 `(3, 5)`
- 출력: `RUKDP`

## 사용법

```bash
python affine_cipher.py decrypt ENJOY 3 5
python affine_cipher.py encrypt RUKDP 3 5
python affine_cipher.py decrypt ENJOY "(3,5)"
```

## 수식

- 암호화: `(ax + b) mod 26`
- 복호화: `a^{-1}(x - b) mod 26`
- 단, `a`는 26과 서로소여야 합니다.

예시:
- `ENJOY` + `(3,5)` → `RUKDP`
