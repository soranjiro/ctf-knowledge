---
title: a fact of CTF
category: crypto
genre: integer-factorization
difficulty: easy
tags:
  - prime-factorization
  - unique-factorization
  - ascii-exponents
source: a-fact-of-CTF/chall.py
solved_at: 2026-05-29
---

# a fact of CTF

## 問題の要点

flag の i 文字目を `ord(c)` として、i 番目の素数をその指数だけ掛けている。

```python
ct *= primes[i] ** (ord(c))
```

素因数分解の一意性により、暗号文の各素因数の指数がそのまま文字コードになる。

## 解き方

```python
ct = int(open("output.txt").read().strip(), 16)
flag = []
for p in primes:
    e = 0
    while ct % p == 0:
        ct //= p
        e += 1
    if e:
        flag.append(chr(e))
print("".join(flag))
```

flag:

```text
Alpaca{prime_factorization_solves_everything}
```

## 連携する知見

- [Crypto](../../../insights/crypto.md)
- [Crypto relations](../../../relations/crypto.md)
