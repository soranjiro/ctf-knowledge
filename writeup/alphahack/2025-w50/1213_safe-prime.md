---
title: Safe Prime
category: crypto
genre: rsa
difficulty: medium
tags:
  - related-primes
  - safe-prime
  - factorization
source: alpacahack:safe-prime
solved_at: 2026-05-29
---

# Safe Prime

## 問題の要点

- RSA modulus が `n = p * q` で、`q = 2p + 1` の safe prime 構造になっている。
- つまり `n = p(2p + 1) = 2p^2 + p`。

## 解き方

二次方程式として `p` を復元する。

```python
# 2p^2 + p - n = 0
p = (-1 + isqrt(1 + 8*n)) // 4
q = 2*p + 1
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, n)
```

## 得られた flag

```text
ctf4b{R3l4ted_pr1m3s_4re_vuLner4ble_n0_maTt3r_h0W_l4rGe_p_1s}
```

## 知見

- safe prime 自体は危険ではないが、`p` と `q` の関係をそのまま公開 modulus に持ち込むと factorization が二次方程式になる。
- RSA では「素数が大きい」より「独立に生成されている」ことが重要。

## 連携する知見

- [RSA](../../../insights/rsa.md)
- [RSA relations](../../../relations/rsa.md)
